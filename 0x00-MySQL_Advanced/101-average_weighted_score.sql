-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;

    -- Declare a cursor to loop through all users
    DECLARE user_cursor CURSOR FOR
    SELECT id FROM users;

    -- Declare a handler to set 'done' when no more rows
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN user_cursor;

    user_loop: LOOP
        -- Fetch each user id
        FETCH user_cursor INTO user_id;

        -- If no more users, exit the loop
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Call the procedure to compute for each user
        CALL ComputeAverageWeightedScoreForUser(user_id);
    END LOOP user_loop;

    CLOSE user_cursor;
END //

DELIMITER ;
