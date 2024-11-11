# # Load the necessary libraries
# library(ngramr)
# library(ggplot2)

# # Query Google Ngram for the word "data" from 1800 to 2000
# ngram_data <- ngram("data", year_start = 1800, year_end = 2000, smoothing = 0)

# # View the first few rows of the data
# head(ngram_data)

# # Plot the data using ggplot2
# ggplot(ngram_data, aes(x = Year, y = Frequency, color = Phrase)) +
#   geom_line() +
#   labs(title = "Google Ngram Viewer Data for 'data'",
#        x = "Year",
#        y = "Frequency") +
#   theme_minimal()

# library(httr)
# library(jsonlite)

# # Construct the URL for the Ngram query
# url <- "https://storage.googleapis.com/books/ngrams/books/datasets/20120701/eng-all-1gram-20120701-utf8.zip"

# # Make the GET request
# response <- GET(url)

# # Check the response status
# if (status_code(response) == 200) {
#   # Parse the JSON content
#   ngram_data <- content(response, "text")
#   ngram_data <- fromJSON(ngram_data)
#   print(head(ngram_data))
# } else {
#   print("Failed to retrieve data.")
# }

library(ngramr)

# Try to use the ngram function again
ngram_data <- ngram("data", year_start = 1800, year_end = 2000, smoothing = 0)

# Check if the data was retrieved successfully
if (!is.null(ngram_data)) {
    head(ngram_data)
} else {
    print("No data retrieved.")
}

# library(httr)

# # Define the Ngram URL for raw data
# url <- "https://books.google.com/ngrams/json?content=A&year_start=1500&year_end=2019&corpus=26&smoothing=3"

# # Fetch the content
# response <- GET(url)
# content <- content(response, "text")

# # Print the raw Ngram data
# print(content)