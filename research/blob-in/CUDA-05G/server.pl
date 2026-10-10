#!/usr/bin/env perl
# SPDX-License-Identifier: MIT
# Independent three-connection Linux SO_PEERCRED / DAC research fixture.
use strict;
use warnings;
use IO::Socket::UNIX;
use Socket qw(SOCK_STREAM SOL_SOCKET);
use Fcntl qw(:mode);
$| = 1;
@ARGV == 2 or die "USAGE server.pl ABSOLUTE_SOCKET ALLOWED_UID\n";
my ($socket_path, $permitted) = @ARGV;
$socket_path =~ m{^/lab/[a-z0-9.-]+\.sock$} or die "BAD_SOCKET_PATH\n";
$permitted =~ /^\d+$/ or die "BAD_ALLOWED_UID\n";
-f $socket_path and die "SOCKET_ALREADY_EXISTS\n";
my $server = IO::Socket::UNIX->new(
    Type => SOCK_STREAM, Local => $socket_path, Listen => 4
) or die "BIND_FAILED $!\n";
chmod 0660, $socket_path or die "CHMOD_SOCKET_FAILED $!\n";
print "READY mode=0660 limit=3\n";
for my $index (0..2) {
    my $client = $server->accept() or die "ACCEPT_FAILED $!\n";
    my $credentials = getsockopt($client, SOL_SOCKET, 17); # Linux SO_PEERCRED
    defined $credentials && length($credentials) == 12 or die "PEER_CREDENTIALS_MISSING\n";
    my ($pid, $uid, $gid) = unpack('i3', $credentials);
    my $command = <$client> // '';
    my $allowed = ($uid == $permitted && $command eq "PING\n") ? 1 : 0;
    print "PEER index=$index uid=$uid gid=$gid decision=" . ($allowed ? 'ALLOWED' : 'DENIED') . "\n";
    my $reply = $allowed ? "ALLOWED\n" : "DENIED\n";
    print {$client} $reply or die "REPLY_FAILED $!\n";
    close $client;
}
close $server;
unlink $socket_path or die "REMOVE_SOCKET_FAILED $!\n";
print "EXIT clean=PASS count=3\n";
