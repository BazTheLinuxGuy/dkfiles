# Web Application: dkfiles &#x1F53B;

**This application**, amateur though it is, is designed to record the contents, location, and owner of our files. The files I am talking about are paper files, the kind you put in hanging file folders.  The files we use are typical home stuff: Credit card records, cable TV guides, medical insurance informatiom. etc.

## About the web application:
  This application is built from a combination of **html**, **cgi** programs written in **python**, styled rather primitively with **css**. Almost *no* javascript is used. I know a little javascript, but not enough to add features to a web page. This may change in the future.

  The data is kept in a **sqlite3** database. The **SQL** records each have eight fields, indexed by a *"file id"* number. Lookups are done with a simple python search in each of the eight fields, compiling a list of every record where the search term is found.

### The lookup feature  
  My husband and I have various filing cabinets and file boxes for files, in the home office and scattered in other rooms. We find the file we're looking for (e.g., dental insurance information) by using the web application's *lookup* feature. 
  
  As a one-time administrative assistant, I remember (with *anguish*) rifling through file folders, trying to find a particular piece of paper, which might have been accidentally filed in an adjacent folder. This lookup method is designed to make finding the right file easy, by a simple search on one or more words, or a part of a word. This returns the full record including where it is. The places it could be are coded as a two-letter abbreviation for the location, e.g. "rf", for the red file cabinet, upper drawer (bottom drawer is "rb").

- ## The **main features** of this application are:
  + --> Main Menu<br />
  + --> Enter a new record <br />
  + --> lookup a record (works via a simple search on any of the eight data fields).<br />
  + --> browse records and optionally edit or delete a record.<br />
  + --> generate a printed report of all records (work in progress)<br />


##### More of this description will be added.
###### __caution! work in progress!__
&copy; 2024, 2025 Kevin R. Baumgarten. All rights reserved. 🍁

