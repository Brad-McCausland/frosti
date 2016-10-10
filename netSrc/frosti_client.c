/* client.c - code for example client program that uses TCP */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <time.h>
#include <math.h>


/*------------------------------------------------------------------------
* Program: client
*
* Purpose: allocate a socket, connect to a server, and print all output
*
* Syntax: client [ host [port] ]
*
* host - name of a computer on which server is executing
* port - protocol port number server is using
*
* Note: Both arguments are optional. If no host name is specified,
* the client uses "localhost"; if no protocol port is
* specified, the client uses the default given by PROTOPORT.
*
*------------------------------------------------------------------------
*/
main( int argc, char **argv) {
	struct hostent *ptrh; /* pointer to a host table entry */
	struct protoent *ptrp; /* pointer to a protocol table entry */
	struct sockaddr_in sad; /* structure to hold an IP address */
	int sd; /* socket descriptor */
	int port; /* protocol port number */
	char *host; /* pointer to host name */
	int n; /* number of characters read */
	char buf[5]; /* buffer for data from the server */

        FILE* logfile = fopen("logs.txt", "a");
        int hour = atoi(&buf[0]);
        int min  = atoi(&buf[3]);
        time_t t = time(NULL);
        struct tm tm = *localtime(&t);

        fprintf(logfile, "%d/%d/%d %d:%d:%d - ", tm.tm_year + 1900, tm.tm_mon, tm.tm_mday,
                                                 tm.tm_hour, tm.tm_min, tm.tm_sec);

	memset((char *)&sad,0,sizeof(sad)); /* clear ip addr structure */
	sad.sin_family = AF_INET; /* set family to Internet */

	if( argc != 3 ) {
		fprintf(stderr,"Error: Wrong number of arguments\n");
		fprintf(stderr,"usage:\n");
		fprintf(stderr,"./client server_address server_port\n");
		exit(EXIT_FAILURE);
	}

	port = atoi(argv[2]); /* convert to binary */
	if (port > 0) /* test for legal value */
		sad.sin_port = htons((u_short)port);
	else {
		fprintf(stderr,"Error: bad port number %s\n",argv[2]);
		exit(EXIT_FAILURE);
	}

	host = argv[1]; /* if host argument specified */

	/* Convert host name to equivalent IP address and copy to sad. */
	ptrh = gethostbyname(host);
	if ( ptrh == NULL ) {
		fprintf(stderr,"Error: Invalid host: %s\n", host);
		exit(EXIT_FAILURE);
	}

	memcpy(&sad.sin_addr, ptrh->h_addr, ptrh->h_length);

	/* Map TCP transport protocol name to protocol number. */
	if ( ((long int)(ptrp = getprotobyname("tcp"))) == 0) {
		fprintf(stderr, "Error: Cannot map \"tcp\" to protocol number");
		exit(EXIT_FAILURE);
	}

	/* Create a socket. */
	sd = socket(PF_INET, SOCK_STREAM, ptrp->p_proto);
	if (sd < 0) {
		fprintf(stderr, "Error: Socket creation failed\n");
		exit(EXIT_FAILURE);
	}

	/* Connect the socket to the specified server. */
	if (connect(sd, (struct sockaddr *)&sad, sizeof(sad)) < 0){ 
		fprintf(logfile, "Action: Alert counterpart is unreachable\n");
		fprintf(stderr,"connect failed\n");
		exit(EXIT_FAILURE);
	}

	/* Receive timestamp for counterpart's most recent log */
	n = recv(sd, buf, sizeof(buf), 0);

  buf[5] = '\0';//null terminate response
  fprintf(logfile, "Message recieved: %s. ", buf);
  buf[2] = '\0';//clobber ':'. Makes minutes and hours readable by the below

  int diff = abs(((hour - tm.tm_hour)*60) - (tm.tm_min - min));

  //raise alert if logs are more than 15 minutes behind
  if(diff > 15){
    fprintf(logfile, "Action: Alert counterpart is up, but not running frosti\n");
  }else{
    fprintf(logfile, "Action: None\n");
  }

  //note '%02d' formatting. This creates leading zeroes to match python dates
  //sprintf(path, "../../logs/%d-%02d-%02d.csv", tm.tm_year+1900, tm.tm_mon+1, tm.tm_mday);
	close(sd);

	exit(EXIT_SUCCESS);
}
