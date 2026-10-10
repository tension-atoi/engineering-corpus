// SPDX-License-Identifier: MIT
// New standalone independent CUDA implementation; NOT the private CUDA-02/03 kernel.
#include <cuda_runtime.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Primitive { int32_t x,y,r,op; };
static constexpr int WIDTH=96, HEIGHT=64, NUM=16, COUNT=WIDTH*HEIGHT;
static_assert(sizeof(Primitive)==16,"primitive ABI differs");
__global__ void compute(const Primitive *p,int32_t *out) {
    int i=blockIdx.x*blockDim.x+threadIdx.x;
    if(i>=COUNT)return;
    int x=i%WIDTH, y=i/WIDTH, acc=0;
    for(int k=0;k<NUM;k++) {
        int dx=x-p[k].x,dy=y-p[k].y;
        int q=dx*dx+dy*dy-p[k].r*p[k].r;
        switch(p[k].op) {
            case 0:if(k==0||q<acc)acc=q;break;
            case 1:if(q>acc)acc=q;break;
            case 2:if(-q>acc)acc=-q;break;
        }
    }
    out[i]=acc;
}
static void fail(const char *where,cudaError_t code){
    fprintf(stderr,"CUDA05H_FAIL %s %s\n",where,cudaGetErrorString(code));exit(2);
}
#define CHECK(step) do {cudaError_t r=(step);if(r!=cudaSuccess)fail(#step,r);}while(0)
int main(int argc,char **argv){
    if(argc!=3){fputs("USAGE: cuda scene.bin cuda-output.bin\n",stderr);return 2;}
    FILE *in=fopen(argv[1],"rb");if(!in){perror("scene open");return 2;}
    Primitive p[NUM];
    if(fread(p,sizeof(Primitive),NUM,in)!=NUM||fgetc(in)!=EOF){fputs("SCENE_BYTE_COUNT_INVALID\n",stderr);return 2;}
    fclose(in);
    if(p[0].op!=0){fputs("SCENE_FIRST_OP_INVALID\n",stderr);return 2;}
    for(auto &v:p)if(v.x<0||v.x>=WIDTH||v.y<0||v.y>=HEIGHT||v.r<3||v.r>19||v.op<0||v.op>2){fputs("SCENE_BOUNDS_INVALID\n",stderr);return 2;}
    int count=0;CHECK(cudaGetDeviceCount(&count));
    if(count<=0){fputs("CUDA_HARDWARE_MISSING\n",stderr);return 2;}
    cudaDeviceProp device{};CHECK(cudaGetDeviceProperties(&device,0));
    fprintf(stderr,"CUDA05H_HARDWARE name=%s major=%d minor=%d devices=%d\n",device.name,device.major,device.minor,count);
    Primitive *deviceP=nullptr;int32_t *deviceOut=nullptr;
    CHECK(cudaMalloc((void**)&deviceP,sizeof(p)));
    CHECK(cudaMalloc((void**)&deviceOut,COUNT*sizeof(int32_t)));
    CHECK(cudaMemcpy(deviceP,p,sizeof(p),cudaMemcpyHostToDevice));
    compute<<<(COUNT+255)/256,256>>>(deviceP,deviceOut);
    CHECK(cudaGetLastError());CHECK(cudaDeviceSynchronize());
    int32_t out[COUNT];CHECK(cudaMemcpy(out,deviceOut,sizeof(out),cudaMemcpyDeviceToHost));
    CHECK(cudaFree(deviceP));CHECK(cudaFree(deviceOut));
    FILE *dest=fopen(argv[2],"wb");if(!dest){perror("output open");return 2;}
    if(fwrite(out,sizeof(out),1,dest)!=1||fclose(dest)!=0){fputs("OUTPUT_WRITE_FAILED\n",stderr);return 2;}
    fprintf(stderr,"CUDA05H_DISPATCH_COMPLETED output_samples=%d\n",COUNT);
    return 0;
}
