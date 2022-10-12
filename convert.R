# reads in json file from the ./data directory and converts it to a csv file

# install.packages("rjson")
library("rjson")

input_file <- "./data/Stephanie User 4681 - 2958.json"
output_file <- "./converted/Stephanie User 4681 - 2958.csv"

json <- fromJSON(file = input_file)

# creating dataframe from json file, will export to csv
headers <- c("file", "title", "google", "identifiable_yes", "identifiable_no", "identifiable_withdetectivework",
             "diversity_none", "diversity_bipoc", "diversity_woman", "diversity_lgbt", "diversity_nonchristian",
             "diversity_disability", "diversity_other", "diversity_ambiguous")

df <- data.frame(matrix(ncol = length(headers), nrow = 0))
colnames(df) <- headers

# loop through _via_img_metadata and add to dataframe
for (i in 1:length(json$"_via_img_metadata")) {
  file <- json$"_via_img_metadata"[[i]]$filename
  title <- json$"_via_img_metadata"[[i]]$file_attributes$title
  google <- json$"_via_img_metadata"[[i]]$file_attributes$google

  if ("identifiable" %in% names(json$"_via_img_metadata"[[i]]$file_attributes)) {
    identifiable <- json$"_via_img_metadata"[[i]]$file_attributes$identifiable
  } else {
    identifiable <- ""
  }
  identifiable_yes <- as.integer(identifiable == "yes")
  identifiable_no <- as.integer(identifiable == "no")
  identifiable_withdetectivework <- as.integer(identifiable == "withdetectivework")


  diversity_none <- as.integer("none" %in% names(json$"_via_img_metadata"[[i]]$file_attributes$diversity))
  diversity_bipoc <- as.integer("bipoc" %in% names(json$"_via_img_metadata"[[i]]$file_attributes$diversity))
  diversity_woman <- as.integer("woman" %in% names(json$"_via_img_metadata"[[i]]$file_attributes$diversity))
  diversity_lgbt <- as.integer("lgbt" %in% names(json$"_via_img_metadata"[[i]]$file_attributes$diversity))
  diversity_nonchristian <- as.integer("non-christian" %in% names(json$"_via_img_metadata"[[i]]$file_attributes$diversity))
  diversity_disability <- as.integer("disability" %in% names(json$"_via_img_metadata"[[i]]$file_attributes$diversity))
  diversity_other <- as.integer("other" %in% names(json$"_via_img_metadata"[[i]]$file_attributes$diversity))
  diversity_ambiguous <- as.integer("ambiguous" %in% names(json$"_via_img_metadata"[[i]]$file_attributes$diversity))
  # create new row from data and add it to the df
  new_row <- data.frame(file, title, google, identifiable_yes, identifiable_no, identifiable_withdetectivework,
                        diversity_none, diversity_bipoc, diversity_woman, diversity_lgbt, diversity_nonchristian,
                        diversity_disability, diversity_other, diversity_ambiguous)
  df <- rbind(df, new_row)
}
# write the df to a csv with utf8 encoding
write.csv(df, file = output_file, row.names = FALSE, fileEncoding = "UTF-8")

