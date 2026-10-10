// SPDX-License-Identifier: MIT
// Independent native Vulkan compute implementation. No private Rust/CUDA code.
#include <vulkan/vulkan.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define COUNT 6144u
#define SCENE_BYTES 256u
#define OUTPUT_BYTES (COUNT*4u)
#define ENSURE(x,why) do{if(!(x)){fprintf(stderr,"CUDA05H_VULKAN_FAIL %s\n",why);exit(3);}}while(0)
#define VK(step) do{VkResult r=(step);if(r!=VK_SUCCESS){fprintf(stderr,"CUDA05H_VULKAN_ERROR %s result=%d\n",#step,r);exit(3);}}while(0)
static unsigned char *load(const char *path,size_t expected){
    FILE *f=fopen(path,"rb");ENSURE(f,"file_open");
    unsigned char *b=malloc(expected);ENSURE(b,"alloc_file");
    ENSURE(fread(b,1,expected,f)==expected&&fgetc(f)==EOF,"file_size");
    ENSURE(fclose(f)==0,"file_close");return b;
}
typedef struct {VkBuffer buffer;VkDeviceMemory memory;void *mapped;} HostBuffer;
static HostBuffer make_buffer(VkPhysicalDevice phy,VkDevice dev,VkDeviceSize size,VkBufferUsageFlags usage){
    HostBuffer out={0};VkBufferCreateInfo b={.sType=VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO,
        .size=size,.usage=usage,.sharingMode=VK_SHARING_MODE_EXCLUSIVE};
    VK(vkCreateBuffer(dev,&b,NULL,&out.buffer));
    VkMemoryRequirements req;vkGetBufferMemoryRequirements(dev,out.buffer,&req);
    VkPhysicalDeviceMemoryProperties properties;vkGetPhysicalDeviceMemoryProperties(phy,&properties);
    uint32_t idx=UINT32_MAX;
    for(uint32_t i=0;i<properties.memoryTypeCount;i++){
       VkMemoryPropertyFlags flags=properties.memoryTypes[i].propertyFlags;
       if((req.memoryTypeBits&(1u<<i))&&
          (flags & (VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT|VK_MEMORY_PROPERTY_HOST_COHERENT_BIT))==
                    (VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT|VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)){
           idx=i;break;
       }
    }
    ENSURE(idx!=UINT32_MAX,"host_coherent_memory_unavailable");
    VkMemoryAllocateInfo ai={.sType=VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO,
        .allocationSize=req.size,.memoryTypeIndex=idx};
    VK(vkAllocateMemory(dev,&ai,NULL,&out.memory));
    VK(vkBindBufferMemory(dev,out.buffer,out.memory,0));
    VK(vkMapMemory(dev,out.memory,0,size,0,&out.mapped));
    return out;
}
static void free_buffer(VkDevice dev,HostBuffer *p){
    vkUnmapMemory(dev,p->memory);vkDestroyBuffer(dev,p->buffer,NULL);
    vkFreeMemory(dev,p->memory,NULL);
}
int main(int argc,char **argv){
    ENSURE(argc==4,"usage: vulkan primitives.bin compute.spv output.bin");
    unsigned char *scene=load(argv[1],SCENE_BYTES);
    int32_t *primitive=(int32_t*)scene;
    ENSURE(primitive[3]==0,"first_op_invalid");
    for(int i=0;i<16;i++){
      int32_t x=primitive[i*4],y=primitive[i*4+1],r=primitive[i*4+2],op=primitive[i*4+3];
      ENSURE(x>=0&&x<96&&y>=0&&y<64&&r>=3&&r<=19&&op>=0&&op<=2,"scene_invalid");
    }
    FILE *code=fopen(argv[2],"rb");ENSURE(code,"open_spirv");
    ENSURE(fseek(code,0,SEEK_END)==0,"seek_spirv");long len=ftell(code);
    ENSURE(len>0&&len<1048576&&(len%4)==0,"spirv_length");
    rewind(code);uint32_t *spv=malloc((size_t)len);ENSURE(spv,"alloc_spv");
    ENSURE(fread(spv,1,(size_t)len,code)==(size_t)len,"read_spirv");
    fclose(code);
    VkApplicationInfo app={.sType=VK_STRUCTURE_TYPE_APPLICATION_INFO,
        .pApplicationName="CUDA05H-Research",.apiVersion=VK_API_VERSION_1_0};
    VkInstanceCreateInfo ici={.sType=VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,.pApplicationInfo=&app};
    VkInstance instance;VK(vkCreateInstance(&ici,NULL,&instance));
    uint32_t n=0;VK(vkEnumeratePhysicalDevices(instance,&n,NULL));
    ENSURE(n>0,"no_vulkan_physical_devices");
    VkPhysicalDevice *devices=calloc(n,sizeof(*devices));ENSURE(devices,"devices_alloc");
    VK(vkEnumeratePhysicalDevices(instance,&n,devices));
    VkPhysicalDevice phy=VK_NULL_HANDLE;uint32_t family=UINT32_MAX;
    VkPhysicalDeviceProperties chosen={0};
    for(uint32_t i=0;i<n && phy==VK_NULL_HANDLE;i++){
        VkPhysicalDeviceProperties prop;vkGetPhysicalDeviceProperties(devices[i],&prop);
        if(prop.deviceType!=VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU &&
           prop.deviceType!=VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU)continue;
        uint32_t m=0;vkGetPhysicalDeviceQueueFamilyProperties(devices[i],&m,NULL);
        VkQueueFamilyProperties *families=calloc(m,sizeof(*families));ENSURE(families,"families_alloc");
        vkGetPhysicalDeviceQueueFamilyProperties(devices[i],&m,families);
        for(uint32_t j=0;j<m;j++)if(families[j].queueFlags&VK_QUEUE_COMPUTE_BIT){
            phy=devices[i];family=j;chosen=prop;break;
        }
        free(families);
    }
    free(devices);ENSURE(phy!=VK_NULL_HANDLE,"no_real_hardware_gpu_vulkan_compute_adapter");
    fprintf(stderr,"CUDA05H_VULKAN_HARDWARE name=%s vendor=%u device=%u type=%u\n",
        chosen.deviceName,chosen.vendorID,chosen.deviceID,chosen.deviceType);
    float priority=1.0f;
    VkDeviceQueueCreateInfo qci={.sType=VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO,
        .queueFamilyIndex=family,.queueCount=1,.pQueuePriorities=&priority};
    VkDeviceCreateInfo dci={.sType=VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO,
        .queueCreateInfoCount=1,.pQueueCreateInfos=&qci};
    VkDevice device;VK(vkCreateDevice(phy,&dci,NULL,&device));
    VkQueue queue;vkGetDeviceQueue(device,family,0,&queue);
    HostBuffer input=make_buffer(phy,device,SCENE_BYTES,VK_BUFFER_USAGE_STORAGE_BUFFER_BIT);
    HostBuffer output=make_buffer(phy,device,OUTPUT_BYTES,VK_BUFFER_USAGE_STORAGE_BUFFER_BIT);
    memcpy(input.mapped,scene,SCENE_BYTES);memset(output.mapped,0,OUTPUT_BYTES);free(scene);
    VkDescriptorSetLayoutBinding bindings[2]={{.binding=0,.descriptorType=VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,
         .descriptorCount=1,.stageFlags=VK_SHADER_STAGE_COMPUTE_BIT},
        {.binding=1,.descriptorType=VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,.descriptorCount=1,
         .stageFlags=VK_SHADER_STAGE_COMPUTE_BIT}};
    VkDescriptorSetLayoutCreateInfo dlci={.sType=VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO,
        .bindingCount=2,.pBindings=bindings};
    VkDescriptorSetLayout layout;VK(vkCreateDescriptorSetLayout(device,&dlci,NULL,&layout));
    VkPipelineLayoutCreateInfo plci={.sType=VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO,
        .setLayoutCount=1,.pSetLayouts=&layout};
    VkPipelineLayout pipelineLayout;VK(vkCreatePipelineLayout(device,&plci,NULL,&pipelineLayout));
    VkShaderModuleCreateInfo smci={.sType=VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO,
        .codeSize=(size_t)len,.pCode=spv};
    VkShaderModule shader;VK(vkCreateShaderModule(device,&smci,NULL,&shader));free(spv);
    VkPipelineShaderStageCreateInfo stage={.sType=VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO,
        .stage=VK_SHADER_STAGE_COMPUTE_BIT,.module=shader,.pName="main"};
    VkComputePipelineCreateInfo cpci={.sType=VK_STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO,
        .stage=stage,.layout=pipelineLayout};
    VkPipeline pipeline;VK(vkCreateComputePipelines(device,VK_NULL_HANDLE,1,&cpci,NULL,&pipeline));
    VkDescriptorPoolSize poolSize={.type=VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,.descriptorCount=2};
    VkDescriptorPoolCreateInfo dpci={.sType=VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO,
        .maxSets=1,.poolSizeCount=1,.pPoolSizes=&poolSize};
    VkDescriptorPool pool;VK(vkCreateDescriptorPool(device,&dpci,NULL,&pool));
    VkDescriptorSetAllocateInfo dsai={.sType=VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO,
        .descriptorPool=pool,.descriptorSetCount=1,.pSetLayouts=&layout};
    VkDescriptorSet set;VK(vkAllocateDescriptorSets(device,&dsai,&set));
    VkDescriptorBufferInfo bufferInfo[2]={{.buffer=input.buffer,.offset=0,.range=SCENE_BYTES},
        {.buffer=output.buffer,.offset=0,.range=OUTPUT_BYTES}};
    VkWriteDescriptorSet writes[2]={{.sType=VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET,
       .dstSet=set,.dstBinding=0,.descriptorCount=1,
       .descriptorType=VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,.pBufferInfo=&bufferInfo[0]},
       {.sType=VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET,.dstSet=set,.dstBinding=1,
       .descriptorCount=1,.descriptorType=VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,
       .pBufferInfo=&bufferInfo[1]}};
    vkUpdateDescriptorSets(device,2,writes,0,NULL);
    VkCommandPoolCreateInfo poolCI={.sType=VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO,
        .queueFamilyIndex=family};
    VkCommandPool cmdPool;VK(vkCreateCommandPool(device,&poolCI,NULL,&cmdPool));
    VkCommandBufferAllocateInfo cbai={.sType=VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO,
        .commandPool=cmdPool,.level=VK_COMMAND_BUFFER_LEVEL_PRIMARY,.commandBufferCount=1};
    VkCommandBuffer cb;VK(vkAllocateCommandBuffers(device,&cbai,&cb));
    VkCommandBufferBeginInfo begin={.sType=VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO};
    VK(vkBeginCommandBuffer(cb,&begin));
    vkCmdBindPipeline(cb,VK_PIPELINE_BIND_POINT_COMPUTE,pipeline);
    vkCmdBindDescriptorSets(cb,VK_PIPELINE_BIND_POINT_COMPUTE,pipelineLayout,0,1,&set,0,NULL);
    vkCmdDispatch(cb,(COUNT+63u)/64u,1,1);
    VkMemoryBarrier barrier={.sType=VK_STRUCTURE_TYPE_MEMORY_BARRIER,
        .srcAccessMask=VK_ACCESS_SHADER_WRITE_BIT,.dstAccessMask=VK_ACCESS_HOST_READ_BIT};
    vkCmdPipelineBarrier(cb,VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,VK_PIPELINE_STAGE_HOST_BIT,
        0,1,&barrier,0,NULL,0,NULL);
    VK(vkEndCommandBuffer(cb));
    VkFenceCreateInfo fci={.sType=VK_STRUCTURE_TYPE_FENCE_CREATE_INFO};
    VkFence fence;VK(vkCreateFence(device,&fci,NULL,&fence));
    VkSubmitInfo submit={.sType=VK_STRUCTURE_TYPE_SUBMIT_INFO,
        .commandBufferCount=1,.pCommandBuffers=&cb};
    VK(vkQueueSubmit(queue,1,&submit,fence));
    VkResult waited=vkWaitForFences(device,1,&fence,VK_TRUE,30000000000ull);
    ENSURE(waited==VK_SUCCESS,"compute_fence_timeout_or_error");
    FILE *dest=fopen(argv[3],"wb");ENSURE(dest,"output_open");
    ENSURE(fwrite(output.mapped,1,OUTPUT_BYTES,dest)==OUTPUT_BYTES&&fclose(dest)==0,"output_write");
    fprintf(stderr,"CUDA05H_VULKAN_DISPATCH_COMPLETED output_samples=%u\n",COUNT);
    vkDestroyFence(device,fence,NULL);
    vkDestroyCommandPool(device,cmdPool,NULL);
    vkDestroyDescriptorPool(device,pool,NULL);
    vkDestroyPipeline(device,pipeline,NULL);
    vkDestroyShaderModule(device,shader,NULL);
    vkDestroyPipelineLayout(device,pipelineLayout,NULL);
    vkDestroyDescriptorSetLayout(device,layout,NULL);
    free_buffer(device,&input);free_buffer(device,&output);
    vkDestroyDevice(device,NULL);vkDestroyInstance(instance,NULL);
    return 0;
}
