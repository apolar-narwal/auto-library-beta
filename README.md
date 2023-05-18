# auto-library-beta
a simple automated library program in python to lend and return books as well as keep a customizable catalogue. this program is optimized to be used by libraries and schools who may not have the resources or faculty to set up a proper library. this program attempts to fix that problem by being easily adaptable to fit the needs of (hopefully) any type of library. i originally made this for my school, but i'm hoping others can also benefit from it. there will be a tutorial and explanation of all of its features coming soon. this is a beta, so some things may not work as intended, but for right now all of its core functions are tried and tested.
 
 features as of right now (may 18 2023)
 - catalogues books based on user input to a text file (can be customized but right now its title, author, and isbn)
 - assigns a five digit code to each book to account for duplicates
 - automates both lending and returning. the current entry fields for both of these actions are email, name, and the book's five digit code, but it can be easily changed in the program
 - keeps an updating log of all actions
 - keeps an updating log of lenders
 - tracks book availibility in a text file that can be viewed by library staff and lenders
 - automatically sends out emails to an administrator and the lender to notify them of overdue books and returns. this is also easily customizable and can be omitted altogether 
 - two week overdue timer (also customizable)
 - simple gui that im currently working on beautifying 
 - admin website that basically just displays, log, lenders, and book list. the reason im not making a catalogue search or something like that is because i want to keep the tactile experience of searching for a book in a physical library
