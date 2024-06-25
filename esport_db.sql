-- Create database if not exists
CREATE DATABASE IF NOT EXISTS esport_db;

-- Use the esport_db database
USE esport_db;

-- Create Player table
CREATE TABLE IF NOT EXISTS Player (
    Player_ID CHAR(6) PRIMARY KEY,
    Nama VARCHAR(50),
    Umur INTEGER,
    Email VARCHAR(30)
);

-- Create Team table
CREATE TABLE IF NOT EXISTS Team (
    Team_ID CHAR(6) PRIMARY KEY,
    Nama_Tim VARCHAR(30),
    Anggota VARCHAR(50),
    Pelatih VARCHAR(50)
);

-- Create Player_Team table
CREATE TABLE IF NOT EXISTS Player_Team (
    Player_Player_ID CHAR(6),
    Team_Team_ID CHAR(6),
    Detail_Player VARCHAR(100),
    PRIMARY KEY (Player_Player_ID, Team_Team_ID),
    FOREIGN KEY (Player_Player_ID) REFERENCES Player(Player_ID),
    FOREIGN KEY (Team_Team_ID) REFERENCES Team(Team_ID)
);

-- Create Salary table
CREATE TABLE IF NOT EXISTS Salary (
    Salary_ID CHAR(6) PRIMARY KEY,
    Jumlah_Pembayar NUMERIC(10,2),
    Tanggal_Pembayar DATE,
    Deskripsi VARCHAR(150),
    Player_Player_ID CHAR(6),
    FOREIGN KEY (Player_Player_ID) REFERENCES Player(Player_ID)
);

-- Create Schedule table
CREATE TABLE IF NOT EXISTS Schedule (
    Schedule_ID CHAR(6) PRIMARY KEY,
    Jenis_Kegiatan VARCHAR(50),
    Tanggal_Kegiatan DATE,
    Waktu_Mulai TIME,
    Waktu_Selesai TIME
);

-- Create Event table
CREATE TABLE IF NOT EXISTS Event (
    Event_ID CHAR(6) PRIMARY KEY,
    Jenis_Event VARCHAR(30),
    Tanggal_Event DATE,
    Deskripsi_Event VARCHAR(20),
    Team_Team_ID CHAR(6),
    Schedule_Schedule_ID CHAR(6),
    FOREIGN KEY (Team_Team_ID) REFERENCES Team(Team_ID),
    FOREIGN KEY (Schedule_Schedule_ID) REFERENCES Schedule(Schedule_ID)
);

-- Create Sponsor table
CREATE TABLE IF NOT EXISTS Sponsor (
    Sponsor_ID CHAR(6) PRIMARY KEY,
    Nama_Sponsor VARCHAR(50),
    Kontak_Sponsor VARCHAR(50)
);

-- Create Sponsor_Team table
CREATE TABLE IF NOT EXISTS Sponsor_Team (
    Sponsor_ID CHAR(6),
    Team_ID CHAR(6),
    PRIMARY KEY (Sponsor_ID, Team_ID),
    FOREIGN KEY (Sponsor_ID) REFERENCES Sponsor(Sponsor_ID),
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID)
);

-- Trigger
-- Enforcing player age
DELIMITER //

CREATE TRIGGER PlayerAgeValidationTrigger
BEFORE INSERT ON Player
FOR EACH ROW
BEGIN
    DECLARE MinimumAge INT DEFAULT 18;  -- Minimum age for players
    
    IF NEW.Umur < MinimumAge THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Player must be at least 18 years old.';
    END IF;
END;
//

DELIMITER ;


-- Enforcing roster number of player limit

DELIMITER //

CREATE TRIGGER TeamRosterLimitTrigger
BEFORE INSERT ON Player_Team
FOR EACH ROW
BEGIN
    DECLARE MaxPlayers INT DEFAULT 10; -- Maximum number of players per team
    DECLARE CurrentPlayerCount INT;

    -- Retrieve current player count for the team
    SELECT COUNT(*) INTO CurrentPlayerCount
    FROM Player_Team
    WHERE Team_Team_ID = NEW.Team_Team_ID;

    -- Check if adding this player exceeds the limit
    IF CurrentPlayerCount >= MaxPlayers THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot add more players. Team roster limit reached.';
    END IF;
END;
//

DELIMITER ;

-- Procedure
-- Calculate player salaries
DELIMITER //

CREATE PROCEDURE CalculatePlayerSalaries()
BEGIN
    DECLARE vPlayerID CHAR(6);
    DECLARE vEventPointsSum DECIMAL(10,2);

    -- Cursor declaration for iterating through PlayerEvents
    DECLARE cur_player_events CURSOR FOR
        SELECT pe.Player_ID, SUM(pe.EventPoints) * 1000 AS EventPointsSum
        FROM PlayerEvents pe
        INNER JOIN Event e ON pe.Event_ID = e.Event_ID
        WHERE e.Tanggal_event BETWEEN DATE_SUB(LAST_DAY(CURDATE()), INTERVAL 1 MONTH) + INTERVAL 1 DAY AND LAST_DAY(CURDATE())
        GROUP BY pe.Player_ID;

    -- Declare handlers for exceptions
    DECLARE CONTINUE HANDLER FOR NOT FOUND
    BEGIN
        -- No more rows in the cursor
    END;

    -- Open cursor
    OPEN cur_player_events;

    -- Loop through cursor results
    calc_loop: LOOP
        FETCH cur_player_events INTO vPlayerID, vEventPointsSum;
        IF vPlayerID IS NULL THEN
            LEAVE calc_loop;
        END IF;

        -- Update Salary table based on calculated sum
        UPDATE Salary
        SET Jumlah_Pembayaran = vEventPointsSum
        WHERE Player_Player_ID = vPlayerID
        AND Tanggal_Pembayaran = LAST_DAY(CURDATE()) + INTERVAL 1 DAY;
    END LOOP;

    -- Close cursor
    CLOSE cur_player_events;
END;
//

DELIMITER ;

-- Genereate team performance procedure
DELIMITER //

CREATE PROCEDURE GenerateTeamPerformanceReport (
    IN TeamID VARCHAR(6),
    IN ReportPeriod VARCHAR(20) -- 'Monthly', 'Quarterly', or 'Annual'
)
BEGIN
    DECLARE StartDate DATE;
    DECLARE EndDate DATE;

    -- Determine start and end dates based on ReportPeriod
    CASE ReportPeriod
        WHEN 'Monthly' THEN
            SET StartDate = DATE_SUB(LAST_DAY(CURDATE()), INTERVAL 1 MONTH) + INTERVAL 1 DAY;
            SET EndDate = LAST_DAY(CURDATE());
        WHEN 'Quarterly' THEN
            SET StartDate = DATE_SUB(LAST_DAY(CURDATE()), INTERVAL 3 MONTH) + INTERVAL 1 DAY;
            SET EndDate = LAST_DAY(CURDATE());
        WHEN 'Annual' THEN
            SET StartDate = DATE_SUB(LAST_DAY(CURDATE()), INTERVAL 1 YEAR) + INTERVAL 1 DAY;
            SET EndDate = LAST_DAY(CURDATE());
        ELSE
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid ReportPeriod. Supported values are Monthly, Quarterly, or Annual.';
    END CASE;

    -- Execute query based on ReportPeriod
    IF ReportPeriod = 'Monthly' OR ReportPeriod = 'Quarterly' OR ReportPeriod = 'Annual' THEN
        SELECT t.Nama_Tim, p.Nama, SUM(e.Points) AS TotalPoints
        FROM Team t
        JOIN Player_Team pt ON t.Team_ID = pt.Team_Team_ID
        JOIN Player p ON pt.Player_Player_ID = p.Player_ID
        JOIN PlayerEvents e ON p.Player_ID = e.Player_ID
        JOIN Event ev ON e.Event_ID = ev.Event_ID
        WHERE t.Team_ID = TeamID
        AND ev.Tanggal_event BETWEEN StartDate AND EndDate
        GROUP BY t.Nama_Tim, p.Nama
        ORDER BY TotalPoints DESC;
    END IF;
END;
//

DELIMITER ;

-- Functions



-- Insert sample data into tables
-- INSERT INTO Player VALUES ('P001', 'Alice', 25, 'alice@example.com');
-- INSERT INTO Player VALUES ('P002', 'Bob', 30, 'bob@example.com');
-- INSERT INTO Team VALUES ('T001', 'Team A', 'Alice, Bob', 'Coach A');
-- INSERT INTO Player_Team VALUES ('P001', 'T001', 'Detail 1');
-- INSERT INTO Player_Team VALUES ('P002', 'T001', 'Detail 2');
-- INSERT INTO Salary VALUES ('S001', 5000.00, '2024-01-01', 'Monthly Salary', 'P001');
-- INSERT INTO Salary VALUES ('S002', 6000.00, '2024-01-01', 'Monthly Salary', 'P002');
-- INSERT INTO Schedule VALUES ('SC001', 'Training', '2024-06-21', '08:00:00', '10:00:00');
-- INSERT INTO Event VALUES ('E001', 'Match', '2024-06-22', 'Quarter Finals', 'T001', 'SC001');
-- INSERT INTO Sponsor VALUES ('SP001', 'Sponsor A', 'contact@sponsor.com');
-- INSERT INTO Sponsor_Team VALUES ('SP001', 'T001');
