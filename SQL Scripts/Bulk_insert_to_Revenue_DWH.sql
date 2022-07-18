BULK INSERT Revenue_DWH
FROM 'C:\Users\Nada\Documents\Orange\Revenue-Tech-DWH-Tables\Revenue_Original\Revenue.csv'
WITH
(
    FIRSTROW = 2, -- as 1st one is header
    FIELDTERMINATOR = ',',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    TABLOCK
)