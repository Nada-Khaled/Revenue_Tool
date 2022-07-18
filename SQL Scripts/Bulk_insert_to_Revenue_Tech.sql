BULK INSERT Revenue_Tech
FROM 'C:\Users\Nada\Documents\Orange\Revenue-Tech-DWH-Tables\Revenue_Tech_v2.csv'
WITH
(
    FIRSTROW = 2, -- as 1st one is header
    FIELDTERMINATOR = ';',  --CSV field delimiter
    ROWTERMINATOR = '|',   --Use to shift the control to next row
    TABLOCK
)