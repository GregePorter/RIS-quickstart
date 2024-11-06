df <- data.frame(
                 c(800, 450, 100, 150),
                 c(800, 450, 100, 150)
                 )

print(df)
write.csv(df, "~/Projects/RIS-quickstart/test_output.csv", row.names=FALSE)
