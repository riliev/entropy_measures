# Helper functions for social network analysis

matrix_to_edge_list <- function(input_df, id_col) {
  #takes an incidence or adjencency matrix and builds an edge list
  # each column name except id_col is considered a node
  # NAs and 0s are considered lack of relationship
  #input_df = engagers_list_df
  #id_col = "id"
  
  col_names <- names(input_df)[!names(input_df) %in% id_col]
  v1<- c()
  v2 <- c()
  for (col_name in col_names){
    v1 <- c(v1,input_df[,id_col])
    buffer_vect <- input_df[,col_name]
    buffer_vect[!is.na(buffer_vect)] <- col_name
    v2 <- c(v2,buffer_vect)
  }
  edge_list <- data.frame(v1,v2)
  edge_list <- edge_list[!is.na(edge_list$v2),]
  return(edge_list)
}

vector_to_similarity_matrix <- function(in_vect) {
  # takes a vector, and returns a data frame with rows
  # comapring each element to each other element
  #in_vect = c(1,2,3,4,5)
  orig_index_vect <- 1:length(in_vect)
  new_index_vect <- 1:length(in_vect)
  
  #initialize a data frame which will have two indices and two values
  comparison_df <- data.frame(
    index_1 = orig_index_vect,
    index_2 = new_index_vect,
    value_1 = in_vect,
    value_2 = in_vect
  )
  for (j in 2:length(in_vect)-1){
    new_index_vect <- c(
      orig_index_vect[(length(orig_index_vect)-j+1):(length(orig_index_vect))], 
      orig_index_vect[1:(length(orig_index_vect)-j)])
    buffer_df <- data.frame(
      index_1 = orig_index_vect,
      index_2 = new_index_vect,
      value_1 = in_vect,
      value_2 = in_vect[new_index_vect]
    )
    comparison_df <- rbind(comparison_df, buffer_df)
  }
  return(comparison_df)
}

similarity_matrix <- function(input_df, id_col, var_col ) {
  # computes a similarity matrix between subjects defined in the 
  # id column, for variable var_col. If the measures is numeric,
  # it measures, distance, if measure is categorical, it measures overlap
  #input_df = data.frame(
  #   id = c(1,2,3), 
  #    cat = c("a","b", "c"), 
  #    cont = c(1,2,3)
  #  )
  #id_col = "id"
  #var_col = "cat"
  
  buffer_df <- vector_to_similarity_matrix(input_df[,var_col])
  buffer_df[buffer_df[,"index_1"] == buffer_df[,"index_2"], c("value_1","value_2")] <- c(NA, NA)
  if (is.numeric(input_df[,var_col])) {
    comparison_vect <- (buffer_df[,3] - buffer_df[,4]) %>% abs()
  } else {
    #categorical data comparison: 0 if the same, 1 otherwise
    comparison_vect <- (buffer_df[,3] == buffer_df[,4])
    comparison_vect <- ifelse(comparison_vect,0,1)
  }
  long_index <- input_df[, id_col]
  out_df <- data.frame(
    index_1 = long_index[buffer_df[,1]],
    index_2 = long_index[buffer_df[,2]],
    val_1 = buffer_df[,3],
    val_2 = buffer_df[,4],
    simil_dist = comparison_vect
  )
  return(out_df)
}

merge_edge_list <- function(edge_df1, core_df1, core_var_name, id_var = "id", to_var = "TO", from_var = "FROM") {
  # merges a variable from core_var_name intd the edge list,
  # once based on FROM, and once based on TO
  # the edge list should have TO and FROM columns, the core_df should have id and variable values
  
  # testing
  #edge_df1 <- edge_list_df
  #core_df1 <- core_part_df
  #core_var_name <- "Denomination"
  
  edge_df1_mrg <- edge_df1
  core_df1_buff <- core_df1[,c(id_var, core_var_name)]
  
  
  names(core_df1_buff)[names(core_df1_buff) == id_var] <- from_var
  names(core_df1_buff)[names(core_df1_buff) == core_var_name] <- paste0("core_var_FROM")
  edge_df1_mrg <- merge(edge_df1_mrg, core_df1_buff, by = from_var, all.x = TRUE, all.y = FALSE)
  
  core_df1_buff <- core_df1[,c(id_var, core_var_name)]
  names(core_df1_buff)[names(core_df1_buff) == id_var] <- to_var
  names(core_df1_buff)[names(core_df1_buff) == core_var_name] <- paste0("core_var_TO")
  edge_df1_mrg <- merge(edge_df1_mrg, core_df1_buff, by = to_var, all.x = TRUE, all.y = FALSE)
  
  return(edge_df1_mrg)
  
}

bootstrap_test <- function(to_vect, from_vect, n_epoch = 10000) {
  # function which simulates random distribution of from links
  # keeps the to_vect constant, and resamples the from vect, and they computes overlap
  # works only with categorical variables (gender, school, etc)
  
  # in about 1/n cases, a person will choose herself. 
  # To avoid this we will need a much more complex randomization, and since this number is 
  # negligable, we will ignore it for now. Morever, this problem only increases the p-values, 
  # so we will not err in the direction of Type I error (false positive).
  
  #returns mean overlpap, and p-value of this overlap being observed by chance 
  # (given the initial distribution of TO and FROM nodes)
  
  # testing
  #to_vect <- edge_list_mrg$core_var_TO
  #from_vect <- edge_list_mrg$core_var_FROM
  
  output <- list()
  same_value_vect <- ifelse(from_vect == to_vect, 1,0)
  perc_same <- sum(same_value_vect, na.rm = TRUE) / sum(!is.na(same_value_vect))
  perc_same <- round(perc_same*100, 2)
  output$mean_overlap <- perc_same
  
  test_vect <- c()
  for (j in 1:n_epoch) {
    vec1 <- from_vect
    vec2 <- sample(to_vect, length(to_vect), replace = FALSE, prob = NULL)
    same_value_vect_test <- ifelse(vec1 == vec2, 1,0)
    perc_same_test <- 
      sum(same_value_vect_test, na.rm = TRUE) / sum(!is.na(same_value_vect_test))
    perc_same_test <- 
      perc_same_test*100
    test_vect <- c(test_vect, perc_same_test)
  }
  mc_p <- sum(test_vect > output$mean_overlap)/length(test_vect) # this is the p-value from the monte carlo simulation
  if (mc_p <.00001) {mc_p = 0.001}
  output$p_value <- mc_p
  return(output)
}

