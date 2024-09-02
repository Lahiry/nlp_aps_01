# NLP APS1

## Most Relevant Trip Advisor Restaurants 🍝🦉

The goal of this NLP project was to develop an API that receives a query and returns the most relevant restaurants related to that input. For this project I decided to use Trip Advisor as a source for my web scrapper to gather the data and assemble my database. All restaurants found in the database are from São Paulo, SP, Brazil and the reviews are real customer's reviews.

## Running the Project with Docker

```bash
docker build -t nlp_api .
docker run -d -p 1234:8888 nlp_api
```

## Test queries
1. sushi -> yield 10 results
2. hambúrguer -> yield some, but less than 10 results
3. maravilhoso -> yield results that are not that obvious: the 5 most relevant restaurants for this query have all different cuisines styles

## Authors 

Raphael Lahiry Cabilio
