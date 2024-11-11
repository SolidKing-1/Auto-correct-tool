# Load necessary libraries
library(httr)
library(jsonlite)
library(dplyr)

# Function to get n-gram data and calculate the average frequency from Google Ngram Viewer
get_ngram_average <- function(ngram, start_year, end_year) {
  url <- paste0("https://books.google.com/ngrams/json?content=", ngram, "&year_start=", start_year, "&year_end=", end_year, "&corpus=26&smoothing=0")
  response <- GET(url)
  
  # Check if the response is valid
  if (response$status_code != 200) {
    stop("Error fetching data from Google Ngram Viewer.")
  }
  
  # Extract the content from the response as JSON
  content <- content(response, "text")
  data <- fromJSON(content)

  # Check if data is empty
  if (length(data) == 0) {
    return(NULL)  # Return NULL if no data is found
  }

  # Extract the timeseries and calculate the average frequency
  timeseries <- unlist(data$timeseries)
  avg_frequency <- mean(timeseries)

  # Return a data frame with the n-gram and its average frequency
  df <- data.frame(ngram = ngram, avg_frequency = avg_frequency)
  
  return(df)
}

# Specify the years for your analysis
start_year <- 2000
end_year <- 2022

# Create an empty data frame to store all results
all_results <- data.frame()

# List all files from a to z
word_files <- list.files(pattern = "_words.txt")

# Process each word file (a_words.txt, b_words.txt, etc.)
for (file in word_files) {
  # Read the words from the current file
  words <- suppressWarnings(readLines(file, encoding = "UTF-8"))
  
  # Loop through each word and get n-gram average frequency
  for (word in words) {
    # Remove potential empty lines
    word <- trimws(word)
    
    if (word != "") {
      # Get the average n-gram frequency for the current word
      ngram_data <- get_ngram_average(word, start_year, end_year)
      
      # Check if data was found and bind it to the results
      if (!is.null(ngram_data)) {
        # Bind the new data to the results data frame
        all_results <- rbind(all_results, ngram_data)
      } else {
        # Print a message to indicate no data was found for the word
        print(paste("No data found for:", word))
      }
      
      Sys.sleep(1)  # To avoid overwhelming the API
    }
  }
}

# Check the structure of the all_results data frame
print("Structure of all_results data frame:")
str(all_results)

# Save the results to a CSV file
write.csv(all_results, "ngram_average_frequency.csv", row.names = FALSE)

# Print a message indicating the file has been saved
print("The average n-gram frequency data has been saved to 'ngram_average_frequency.csv'.")
