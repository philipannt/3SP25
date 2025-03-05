CREATE DATABASE PROJ_ADY;
USE PROJ_ADY;

CREATE TABLE tbl_Xemaychotot (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name_Bike VARCHAR(100),
    Year_Of_Manufacture VARCHAR(4) NULL,
    Distance_of_Bike VARCHAR(50) NULL,
    Nationality VARCHAR(50) NULL,
    Location_bike VARCHAR(200) NULL,
    Listing_time VARCHAR(50) NULL,
    Price VARCHAR(20),
    Price_min VARCHAR(20),
    Price_max VARCHAR(20)
);
DELIMITER //

CREATE PROCEDURE prcInsertDataOfBike(IN json_data JSON)
BEGIN
    INSERT INTO tbl_Xemaychotot (
        Name_Bike, 
        Year_Of_Manufacture,
        Distance_of_Bike,
        Nationality, 
        Location_bike, 
        Listing_time,
        Price, 
        Price_min, 
        Price_max
    )
    SELECT 
        Name_Bike,
        Year_Of_Manufacture,
        Distance_of_Bike,
        Nationality,
        Location_bike,
        Listing_time,
        Price,
        Price_min,
        Price_max
    FROM JSON_TABLE(
        json_data, '$[*]'
        COLUMNS (
            Name_Bike VARCHAR(100) PATH '$.name',
            Year_Of_Manufacture VARCHAR(4) PATH '$.Year_of_manufacture',
            Distance_of_Bike VARCHAR(50) PATH '$.Kilometers_driven',
            Nationality VARCHAR(50) PATH '$.Nationality',
            Location_bike VARCHAR(200) PATH '$.Location',
            Listing_time VARCHAR(50) PATH '$.Listing_time',
            Price VARCHAR(20) PATH '$.price',
            Price_min VARCHAR(20) PATH '$.price_min',
            Price_max VARCHAR(20) PATH '$.price_max'
        )
    ) AS jt;
END //
DELIMITER //

SELECT * FROM tbl_Xemaychotot;