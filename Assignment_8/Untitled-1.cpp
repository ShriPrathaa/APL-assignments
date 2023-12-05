#include <iostream>
#include <math.h>
using namespace std;

bool isPrime(int num) {
    if (num < 2) {
        return false;
    }
    for (int i = 2; i * i <= num; i++) {
        if (num % i == 0) {
            return false;
        }
    }
    return true;
}

int findLargestPrime(int n) {
    for (int i = n; i >= 2; i--) {
        if (isPrime(i)) {
            return i;
        }
    }
    return -1; // No prime number found
}

int main() {
	// your code goes here
	int t,h,n;
	cin>>t;
	for(int i=0;i<t;i++){
	    n=1;
	    cin>>h;
	    h-=findLargestPrime(h);

	    if(h>0){
	    i=log(h)/log(2);
	    if((h+1)==2^(1+i))
	        cout<<(2+i)<<"\n";
	    }  
	    else if((h+1)==2^(i))
	        cout<<(i+1)<<"\n";
	    else
	        cout<<-1<<"\n";
	}
	return 0;
}