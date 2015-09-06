Readme
======

Page Rank - Power Method

How to run?
This is a python code embedded in Ipython notebook. One can use Ipython editor like Canopy to run.
If you dint find suitable editor for IPYNB file, I have enclosed the code's raw python file for reference

Input
=====
The following input shall be given,
1. The base directory for the project
	Ex. srcDir = 'C:\\Stuffs\\Courses\\SocialNetworks\\FinalProject'
2. The file name of network data csv file, with edges represented as comma seperated node values
	Ex. inputFriendsGraph = '\\mutualfriends.csv'
3. The name of the subject or the owner of the Network Graph
	Ex. myName = 'Ashwin Giridharan'
4. Scaling factor to be used in Power Method
	Ex. alpha = 0.75
5. Tolerance factor to be used in Power Method
	Ex. tolerance = 1.0/10000000000.0

Output
======
A file of the format rankComp[alpha]_[tolerance].csv is generated with connections/nodes ranked by Power method and in-degree method.

The following cloumns are reported in the output file
Name	PowerRank	DegreeRank	PowerScore	DegreeCount
