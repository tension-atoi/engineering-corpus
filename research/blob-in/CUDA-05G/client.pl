#!/usr/bin/env perl
# SPDX-License-Identifier: MIT
use strict;
use warnings;
use IO::Socket::UNIX;
use Socket qw(SOCK_STREAM);
@ARGV == 1 or die "USAGE client.pl ABSOLUTE_SOCKET\n";
my $socket = IO::Socket::UNIX->new(Type => SOCK_STREAM, Peer => $ARGV[0]);
$socket or die "CONNECT_FAILED $!\n";
print {$socket} "PING\n" or die "WRITE_FAILED $!\n";
my $response = <$socket> // '';
close $socket;
print $response;
