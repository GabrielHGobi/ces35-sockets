CXX=g++
CXXOPTIMIZE= -O2
CXXFLAGS= -g -Wall -pthread -std=c++11 $(CXXOPTIMIZE)
USERID=cesarmarcondes
#CLASSES=SUA_LIB_COMUM
all: echo-server echo-client multi-thread showip
echo-server: 
	$(CXX) -o $@.exe $^ $(CXXFLAGS) $@.cpp
echo-client: 
	$(CXX) -o $@.exe $^ $(CXXFLAGS) $@.cpp
multi-thread:
	$(CXX) -o $@.exe $^ $(CXXFLAGS) $@.cpp
showip:
	$(CXX) -o $@.exe $^ $(CXXFLAGS) $@.cpp
clean:
	rm -rf *.o *~ *.gch *.swp *.dSYM multi-thread.exe showip.exe echo-server.exe echo-client.exe *.tar.gz
tarball: clean
	tar -cvf lab02-$(USERID).tar.gz *
