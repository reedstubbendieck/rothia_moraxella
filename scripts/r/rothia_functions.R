# function for extracting environmental fit vectors from a matrix using envfit

get_fit_vectors <- function(ordination, matrix, permutations, group_name) {
  # run envfit
  fit <- envfit(ordination, matrix, permutations)
  # pull out the arrow coordinates
  arrow_coordinates <- as_tibble(fit$vectors$arrows*sqrt(fit$vectors$r), rownames=group_name)
  # pull out the r2 values
  r2_values <- as_tibble(fit$vectors$r, rownames=group_name)
  colnames(r2_values) <- c(group_name, "r2")
  # pull out the p values
  p_values <- as_tibble(fit$vectors$pvals, rownames=group_name)
  colnames(p_values) <- c(group_name, "p")
  # merge the data frames
  full_values <- left_join(r2_values, p_values, by=group_name)
  full_values <- left_join(full_values, arrow_coordinates, by=group_name)
  full_values
}
