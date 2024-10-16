-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT;
    DECLARE weighted_sum FLOAT;

    -- Calculate total weight of all projects
    SELECT SUM(weight) INTO total_weight
    FROM projects;

    -- Calculate the weighted sum of scores for the user
    SELECT SUM(c.score * p.weight) INTO weighted_sum
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Update the user's average score
    UPDATE users
    SET average_score = weighted_sum / total_weight
    WHERE id = user_id;
END //

DELIMITER ;
