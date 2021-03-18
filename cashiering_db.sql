-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 18, 2021 at 02:52 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cashiering_db`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_CHECK_CREDENTIALS` (IN `P_USERNAME` VARCHAR(50), IN `P_PASSWORD` VARCHAR(50))  BEGIN 
	SELECT UNAME
			,ROLE_ID
	FROM `USER`
	WHERE UNAME = P_USERNAME
	  AND PSWORD = MD5(MD5(SHA1(`P_PASSWORD`)));
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_CHECK_UNAME_CMS` (IN `P_USERNAME` VARCHAR(50))  BEGIN
	SELECT COUNT(UNAME)
	FROM `USER`
	WHERE UNAME = P_USERNAME;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_DEACT_FUND_TYPE` (IN `P_FNDTYPE` VARCHAR(50))  BEGIN
	UPDATE FUND
	SET IS_ACTIVE = 0
	WHERE UPPER(FUND_TYPE) = UPPER(P_FNDTYPE);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_DEACT_INC_TYPE` (IN `P_INCTYPE` VARCHAR(50))  BEGIN
	UPDATE INCOME
	SET IS_ACTIVE = 0
	WHERE UPPER(INCOME_TYPE) = UPPER(P_INCTYPE);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_DEACT_USER` (IN `P_ID` INT, IN `P_ACT` VARCHAR(50))  BEGIN
	UPDATE `USER`
	SET IS_ACTIVE = IF(P_ACT='deact',0,1)
	WHERE USER_ID = P_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_DONE_DEPOSIT` (IN `P_GROUPID` VARCHAR(50), IN `P_SLIPNUM` VARCHAR(50))  BEGIN 
	UPDATE deposit
	SET `STATUS` = 'DEPOSITED'
		,SLIP_NUM = P_SLIPNUM
		,DATE_DEPOSITED = NOW()
	WHERE GROUP_ID = P_GROUPID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_INSERT_COLLECTION` (IN `P_ORNUM` VARCHAR(50), IN `P_ASSESSED` DECIMAL, IN `P_COLLECTED` DECIMAL, IN `P_STUDNO` VARCHAR(50), IN `P_CLIENT` VARCHAR(50), IN `P_EDUCLEVEL` VARCHAR(50), IN `P_USERID` VARCHAR(50))  BEGIN
	IF P_EDUCLEVEL = '' THEN
		IF P_STUDNO = '' THEN
			SET P_EDUCLEVEL = 'Company';
		END IF;
	END IF;
	IF P_STUDNO = '' THEN
		SET P_STUDNO = NULL;
	END IF;
		
	INSERT INTO collection(OR_NUM, ASSESSED, COLLECTED, STUD_NO, CLIENT_NAME, EDUC_LEVEL, TRANS_DATE, `STATUS`, USER_ID)
	VALUES(P_ORNUM
			,P_ASSESSED
			,P_COLLECTED
			,P_STUDNO
			,P_CLIENT
			,P_EDUCLEVEL
			,CURRENT_TIMESTAMP
			,'PENDING'
			,P_USERID
			);
	UPDATE or_set 
	SET CURR_COUNT = CURR_COUNT - 1
	WHERE ID = (SELECT MAX(ID) FROM or_set);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_INSERT_COLLECTION_BREAKDOWN` (IN `P_ORNUM` VARCHAR(50), IN `P_DESC` VARCHAR(50), IN `P_AMT` NUMERIC)  BEGIN 
	INSERT INTO collection_breakdown(`DESC`, AMT, OR_NUM)
	VALUES(TRIM(P_DESC)
			,P_AMT
			,P_ORNUM);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_INSERT_DEPOSIT` (IN `P_ORNUM` VARCHAR(50), IN `P_GROUPID` VARCHAR(50), IN `P_STATUS` VARCHAR(50), IN `P_DATESCHED` DATETIME, IN `P_NOTES` VARCHAR(255), IN `P_USERID` INT)  BEGIN 
	INSERT INTO deposit(OR_NUM, GROUP_ID, `STATUS`, DATE_SCHEDULED, DATE_UPDATED, NOTES, USER_ID)
	VALUES(P_ORNUM
			,P_GROUPID
			,P_STATUS
			,P_DATESCHED
			,NOW()
			,P_NOTES
			,P_USERID);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_INSERT_OR_SET` (IN `P_START_VAL` VARCHAR(50), IN `P_END_VAL` VARCHAR(50))  BEGIN 
	INSERT INTO OR_SET(OR_NUM_START, OR_NUM_END, DATE_ADDED, ORIG_COUNT, CURR_COUNT)
	VALUES(P_START_VAL
			,P_END_VAL
			,CURRENT_TIMESTAMP
			,(CAST(P_END_VAL AS INT) + 1) - (CAST(P_START_VAL AS INT))
			,(CAST(P_END_VAL AS INT) + 1) - (CAST(P_START_VAL AS INT))
			);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_INSERT_UACS_FUND` (IN `P_CODE` VARCHAR(50), IN `P_DESC` VARCHAR(50))  BEGIN
	INSERT INTO fund(FUND_TYPE, FUND_CODE, DATE_ADDED)
	VALUES(P_DESC
			,P_CODE
			,NOW());
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_INSERT_UACS_INC` (IN `P_DESC` VARCHAR(50))  BEGIN
	INSERT INTO income(INCOME_TYPE, DATE_ADDED)
	VALUES(P_DESC
			,NOW());
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_INSERT_UACS_TABLE` (IN `P_FNDTYPE` VARCHAR(50), IN `P_INCTYPE` VARCHAR(50), IN `P_OCODE` VARCHAR(50), IN `P_CODE` VARCHAR(50), IN `P_DESC` VARCHAR(50))  BEGIN
	IF P_INCTYPE = 'N/A' THEN
		SET P_INCTYPE = NULL;
	END IF;
	INSERT INTO uacs(UACS_CODE, OLD_CODE, FUND_TYPE, INCOME_TYPE, `DESC`, DATE_ADDED)
	VALUES(P_CODE
			,P_OCODE
			,P_FNDTYPE
			,P_INCTYPE
			,P_DESC
			,NOW());
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_INSERT_USER_CMS` (IN `P_FNAME` VARCHAR(50), IN `P_MNAME` VARCHAR(50), IN `P_LNAME` VARCHAR(50), IN `P_UNAME` VARCHAR(50), IN `P_EMAIL` VARCHAR(50), IN `P_PSWORD` VARCHAR(50), IN `P_ROLEID` INT)  BEGIN
	INSERT INTO `USER`(`FNAME`, `MNAME`, `LNAME`, `UNAME`, `EMAIL`, `PSWORD`, `DATE_ADDED`, `ROLE_ID`)
	VALUES(`P_FNAME`
			,`P_MNAME`
			,`P_LNAME`
			,`P_UNAME`
			,`P_EMAIL`
			,MD5(MD5(SHA1(`P_PSWORD`)))
			,CURRENT_TIMESTAMP
			,`P_ROLEID`);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_LOAD_ADMIN_DASHBOARD_CARDS` ()  BEGIN
	SELECT
		(
			SELECT COUNT(*)
			FROM `USER`
			WHERE IS_ACTIVE = 1
		) AS TOTAL_USERS,
		(
			SELECT COUNT(*)
			FROM `USER`
			WHERE DATEDIFF(NOW(),DATE_ADDED) <= 30
		) AS NEW_USERS,
		(
			SELECT COUNT(*)
			FROM `USER`
			WHERE IS_ACTIVE = 0
		) AS DEACT_USERS,
		(
			SELECT COUNT(*)
			FROM UACS
			WHERE IS_ACTIVE = 1
		) AS COUNT_UACS;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_LOAD_CERT_TABLE` (IN `P_MONTH` INT)  BEGIN
	SELECT DATE_DEPOSITED
			,SLIP_NUM
			,SUM(COLLECTED)
	FROM DEPOSIT
	INNER JOIN COLLECTION
	ON deposit.OR_NUM = collection.OR_NUM
	WHERE MONTH(DATE_DEPOSITED) = P_MONTH
	GROUP BY deposit.GROUP_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_LOAD_DASHBOARD_CARDS` ()  BEGIN
	SELECT
	(
		SELECT SUM(COLLECTED)
		FROM COLLECTION
		WHERE DATE(TRANS_DATE) = DATE(NOW())
	) AS TODAY_COLLECTION,
	(
		SELECT SUM(COLLECTED)
		FROM COLLECTION
		WHERE EDUC_LEVEL = 'SIS Payment'
			AND DATE(TRANS_DATE) = DATE(NOW())
	) AS TODAY_SIS,
	(
		SELECT SUM(COLLECTED)
		FROM COLLECTION
		WHERE MONTH(TRANS_DATE) = MONTH(NOW())
	) AS MONTH_COLLECTION,
	(
		SELECT SUM(COLLECTED)
		FROM COLLECTION
		WHERE YEAR(TRANS_DATE) = YEAR(NOW())
	) AS YEAR_COLLECTION,
		(
		SELECT COUNT(OR_NUM)
		FROM COLLECTION
		WHERE DATE(TRANS_DATE) = DATE(NOW())
	) AS COUNT_OR_TODAY,
	(
		SELECT COUNT(OR_NUM)
		FROM COLLECTION
		WHERE EDUC_LEVEL = 'SIS Payment'
			AND DATE(TRANS_DATE) = DATE(NOW())
	) AS COUNT_SIS_OR_TODAY;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_LOAD_DEPOSITED` ()  BEGIN
	SELECT deposit.DATE_DEPOSITED
			,deposit.GROUP_ID
			,SUM(collection.COLLECTED)
	FROM DEPOSIT
	INNER JOIN COLLECTION
	ON deposit.OR_NUM = collection.OR_NUM
		AND deposit.`STATUS` = 'DEPOSITED'
	GROUP BY deposit.GROUP_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_LOAD_RADAR_CHART` (IN `P_MONTH` INT)  BEGIN
	SELECT UA.UACS_CODE
			,CB.`DESC`
		   ,CB.AMT AS TOTAL
	FROM uacs AS UA
	INNER JOIN collection_breakdown AS CB
	USING (`DESC`)
	INNER JOIN collection AS CO
	ON CB.OR_NUM = CO.OR_NUM
	WHERE MONTH(CO.TRANS_DATE) = P_MONTH 
   GROUP BY UA.`DESC`;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_REMOVE_SCHED_DEPOSIT` (IN `P_GROUPID` VARCHAR(50))  BEGIN 
	UPDATE COLLECTION
	SET `STATUS` = 'PENDING'
	WHERE OR_NUM IN(SELECT OR_NUM FROM DEPOSIT
						 WHERE GROUP_ID = P_GROUPID);
	DELETE FROM DEPOSIT
	WHERE GROUP_ID = P_GROUPID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SAVE_FOR_REMITTANCE` (IN `P_OR_NUM` VARCHAR(50))  BEGIN
	UPDATE COLLECTION
	SET `STATUS` = 'FOR REMIT'
	WHERE OR_NUM = P_OR_NUM;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_ACCOUNTABLE_FORMS_REPORT` (IN `P_MONTH` INT, IN `P_WAY` VARCHAR(50))  BEGIN 
	IF P_WAY = 'MONTHLY' THEN
		INSERT INTO TMP(TOT_USED)
		SELECT 
			(SELECT COUNT(*)
			  FROM collection 
			  WHERE MONTH(TRANS_DATE) = P_MONTH);
	END IF;
	IF P_WAY = 'CARD' THEN
		SELECT
			 (SELECT COUNT(*)
			  FROM collection 
			  WHERE MONTH(TRANS_DATE) = P_MONTH)
			,(SELECT IFNULL(LPAD(MIN(CAST(OR_NUM AS INT)),LENGTH(OR_NUM),'0'),LPAD('',(SELECT LENGTH(OR_NUM) 
																												 FROM collection 
																												 WHERE OR_NUM = (SELECT MAX(OR_NUM)
																												 					  FROM COLLECTION)),'-'))
			  FROM collection
			  WHERE MONTH(TRANS_DATE) = P_MONTH)
			,(SELECT IFNULL(LPAD(MAX(CAST(OR_NUM AS INT)),LENGTH(OR_NUM),'0'),LPAD('',(SELECT LENGTH(OR_NUM) 
																												 FROM collection 
																												 WHERE OR_NUM = (SELECT MAX(OR_NUM)
																												 					  FROM COLLECTION)),'-'))
			  FROM collection 
			  WHERE MONTH(TRANS_DATE) = P_MONTH
			  		AND DATE(TRANS_DATE) = (SELECT LAST_DAY(CURRENT_TIMESTAMP)))
			,(SELECT COUNT(*)
			  FROM collection 
			  WHERE EDUC_LEVEL = 'SIS PAYMENT'
			  		AND MONTH(TRANS_DATE) = P_MONTH)
			,(SELECT COUNT(*)
			  FROM collection 
			  WHERE EDUC_LEVEL = 'COMPANY'
			  		AND MONTH(TRANS_DATE) = P_MONTH)
			,(SELECT COUNT(*)
			  FROM collection 
			  WHERE EDUC_LEVEL = 'NON-STUDENT'
			  		AND MONTH(TRANS_DATE) = P_MONTH)
			,(SELECT COUNT(*)
			  FROM collection 
			  WHERE EDUC_LEVEL NOT IN('SIS PAYMENT','COMPANY','NON-STUDENT')
			  		AND MONTH(TRANS_DATE) = P_MONTH);
	END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_ALL_RECEIPTS` ()  BEGIN
	SELECT OR_NUM
			,CLIENT_NAME
			,DATE_FORMAT(TRANS_DATE, '%m/%d/%Y')
	FROM collection;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_ALL_UACS_CODE` (IN `P_INCTYPE` VARCHAR(50))  BEGIN
	SELECT UACS_CODE
			,`DESC`
	FROM uacs
	WHERE INCOME_TYPE = P_INCTYPE
		AND IS_ACTIVE = 1;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_ALL_USERS` ()  BEGIN
	SELECT USER_ID
			,FNAME
			,MNAME
			,LNAME
			,UNAME
			,DATE_ADDED
			,IF(ROLE_ID=1, 'Admin', 'Cashier') AS USER_ROLE
			,IS_ACTIVE
	FROM `USER`;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_ALL_USERS2` ()  BEGIN
	SELECT USER_ID
			,FNAME
			,MNAME
			,LNAME
			,UNAME
			,DATE_ADDED
			,IF(ROLE_ID=1, 'Admin', 'Cashier') AS USER_ROLE
			,IS_ACTIVE
	FROM `USER`;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_COLLECTION_LOG` (IN `P_START` DATETIME, IN `P_END` DATETIME)  BEGIN
	SELECT OR_NUM
			,CLIENT_NAME
			,ASSESSED
			,COLLECTED
			,TRANS_DATE
			,UPPER(EDUC_LEVEL)
	FROM collection
	WHERE DATE(TRANS_DATE) BETWEEN DATE(P_START) AND DATE(P_END)
	ORDER BY TRANS_DATE DESC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_COLLECTION_PENDING` (IN `P_START` DATETIME, IN `P_END` DATETIME)  BEGIN
	SELECT OR_NUM
			,CLIENT_NAME
			,ASSESSED
			,COLLECTED
			,TRANS_DATE
			,UPPER(EDUC_LEVEL)
	FROM collection
	WHERE DATE(TRANS_DATE) BETWEEN DATE(P_START) AND DATE(P_END)
		AND `STATUS` = 'PENDING'
	ORDER BY DATE(TRANS_DATE) DESC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_CURRENT_GROUP_ID` ()  BEGIN
	SELECT IF(ISNULL((SELECT COUNT(GROUP_ID) FROM deposit)) = 1
		,(SELECT CONCAT(CAST(YEAR(NOW()) AS CHAR(4)),'-DEPOSIT-00001'))
		,(SELECT CONCAT(CAST(YEAR(NOW()) AS CHAR(4))
							,'-DEPOSIT-'
							,(SELECT LPAD((SELECT SUBSTR((SELECT GROUP_ID 
																	FROM deposit 
																	WHERE DEP_ID = (SELECT MAX(DEP_ID) FROM deposit))
																	,14)) + '1'
																	,5
																	,'0'))))) AS CURRENT_GROUP_ID;			
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_CURRENT_OR` ()  BEGIN
	SELECT IF(ISNULL((SELECT OR_NUM 
						FROM collection WHERE OR_NUM = (SELECT MAX(CAST(OR_NUM AS UNSIGNED))
																  FROM collection)
												AND OR_NUM >= (SELECT MAX(CAST(OR_NUM_START AS UNSIGNED)) FROM OR_SET))) = 1
			,(SELECT OR_NUM_START 
			  FROM or_set 
			  WHERE ID = (SELECT MAX(ID) FROM or_set))
			,(SELECT LPAD(OR_NUM + '1',LENGTH(OR_NUM), '0')
			  FROM collection 
			  WHERE OR_NUM = (SELECT MAX(CAST(OR_NUM AS UNSIGNED)) 
			  						FROM collection)
		  			AND OR_NUM <= (SELECT MAX(CAST(OR_NUM_END AS UNSIGNED)) 
		  								FROM or_set
										WHERE ID = (SELECT MAX(ID) FROM or_set))								  
			 )) AS CURRENT_OR;			  	
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_EMAIL_CREDENTIALS` ()  BEGIN 
	SELECT CASHIER_EMAIL
			,CASHIER_PASS
	FROM EMAIL_CONFIG
	WHERE IS_ACTIVE = 1;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_FNAME_CMS` (IN `P_USERNAME` VARCHAR(50))  BEGIN
	SELECT CONCAT(FNAME,' ',IFNULL(SUBSTRING(MNAME,1,1),''),'.',' ',LNAME) AS FULLNAME
	FROM user
	WHERE UNAME = `P_USERNAME`;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_FUND_TYPE` ()  BEGIN
	SELECT FUND_TYPE		
	FROM fund  
	WHERE IS_ACTIVE = 1;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_INACTIVE_UACS` ()  BEGIN
	SELECT OLD_CODE
			,UACS_CODE
			,`DESC`
	FROM UACS
	WHERE IS_ACTIVE = 0;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_INCOME_TYPE` ()  BEGIN
	SELECT INCOME_TYPE		
	FROM income 
	WHERE IS_ACTIVE = 1;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_MONTHLY_COLLECTION` ()  BEGIN
	SELECT MONTH(TRANS_DATE) AS TRANS_DATE
			,SUM(COLLECTED) AS COLLECTED
	FROM COLLECTION
	WHERE YEAR(TRANS_DATE) = YEAR(NOW())
	GROUP BY MONTH(TRANS_DATE);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_MONTHLY_DEPOSIT` ()  BEGIN
	SELECT MONTH(DATE_DEPOSITED) AS DATE_DEPOSITED
			,SUM(collection.COLLECTED) AS DEPOSIT_AMT
	FROM COLLECTION
	INNER JOIN DEPOSIT
	ON collection.OR_NUM = deposit.OR_NUM
	WHERE deposit.`STATUS` = 'DEPOSITED'
		AND YEAR(DATE_DEPOSITED) = YEAR(NOW())
	GROUP BY MONTH(DATE_DEPOSITED);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_OR_MONTHLY_REPORT` ()  BEGIN
	DROP TABLE IF EXISTS TMP;
	CREATE TEMPORARY TABLE TMP(TOT_USED INT);
	SET @MON = (SELECT MONTH(NOW()));
	SET @IDX = 1;
	WHILE @IDX <= @MON DO
		CALL SP_SELECT_ACCOUNTABLE_FORMS_REPORT(@IDX,'MONTHLY');
		SET @IDX = @IDX + 1;
	END WHILE;
	
	SELECT * FROM TMP;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_RECEIPT_DONUT` ()  BEGIN
	SELECT EDUC_LEVEL
			,COUNT(EDUC_LEVEL)
			,COUNT(EDUC_LEVEL) / (SELECT COUNT(EDUC_LEVEL) FROM collection) * 100 AS PERCENTAGE
	FROM collection
	GROUP BY EDUC_LEVEL;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_SCHEDULED_DEPOSITS` ()  BEGIN
	SELECT deposit.GROUP_ID
			,deposit.DATE_SCHEDULED
			,SUM(collection.COLLECTED)
			,deposit.NOTES
	FROM deposit
	INNER JOIN COLLECTION
	ON deposit.OR_NUM = collection.OR_NUM
		AND deposit.`STATUS` = 'FOR REMIT'
	GROUP BY deposit.GROUP_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_SIS_BAR_CHART` (IN `P_FILTER` VARCHAR(50))  BEGIN
	IF P_FILTER = 'DAILY' THEN
		SET @START_FILTER = (SELECT DATE_SUB(NOW(),INTERVAL 6 DAY));
		SET @END_FILTER = (SELECT DATE_ADD(NOW(), INTERVAL 6 DAY));
		SELECT SUM(COLLECTED)
				,DATE(TRANS_DATE) AS TRANSDATE
		FROM COLLECTION
		WHERE EDUC_LEVEL = 'SIS Payment'
			AND DATE(TRANS_DATE) BETWEEN DATE(@START_FILTER) AND DATE(@END_FILTER)
		GROUP BY TRANSDATE;
	END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_SIS_PAYMENTS_DONE` ()  BEGIN
	SELECT OR_NUM
		,COLLECTED
		,DATE_FORMAT(TRANS_DATE, '%m/%d/%Y') AS TRANS_DATE
	FROM collection
	WHERE EDUC_LEVEL = 'SIS Payment'
		AND OR_NUM IN (SELECT OR_NUM FROM collection_breakdown);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_SIS_PAYMENTS_PENDING` ()  BEGIN
	SELECT OR_NUM
		,COLLECTED
		,DATE_FORMAT(TRANS_DATE, '%m/%d/%Y') AS TRANS_DATE
	FROM collection
	WHERE EDUC_LEVEL = 'SIS Payment'
		AND OR_NUM NOT IN (SELECT OR_NUM FROM COLLECTION_BREAKDOWN);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_SPECIFIC_COLLECTION` (IN `P_ORNUM` VARCHAR(50))  BEGIN
	SELECT OR_NUM
			,CLIENT_NAME
			,STUD_NO
			,DATE_FORMAT(DATE(TRANS_DATE), '%b. %d, %Y') AS TRANS_DATE
			,TIME_FORMAT(TIME(TRANS_DATE), '%h:%i %p') AS TRANS_TIME
			,COLLECTED
	FROM collection
	WHERE OR_NUM = P_ORNUM;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_SPECIFIC_COLLECTION_BREAKDOWN` (IN `P_ORNUM` VARCHAR(50))  BEGIN
	SELECT `DESC`
			,AMT
	FROM collection_breakdown
	WHERE OR_NUM = P_ORNUM;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_SPECIFIC_FUND` (IN `P_FNDTYPE` VARCHAR(50))  BEGIN
	SELECT FUND_CODE
	FROM FUND
	WHERE UPPER(FUND_TYPE) = UPPER(P_FNDTYPE)
		AND IS_ACTIVE = 1;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_SPECIFIC_INCOME` (IN `P_INCTYPE` VARCHAR(50))  BEGIN
	SELECT INCOME_TYPE
	FROM INCOME
	WHERE UPPER(INCOME_TYPE) = UPPER(P_INCTYPE)
		AND IS_ACTIVE = 1;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_SPECIFIC_SIS_CLIENT` (IN `P_ORNUM` VARCHAR(50))  BEGIN
	SELECT CLIENT_NAME
			,TRANS_DATE
	FROM COLLECTION
	WHERE OR_NUM = P_ORNUM;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_SPECIFIC_SIS_DONE` (IN `P_ORNUM` VARCHAR(50))  BEGIN
	SELECT `DESC`
			,AMT
	FROM COLLECTION_BREAKDOWN
	WHERE OR_NUM = P_ORNUM;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_STUDENT_NAME` (IN `P_STUDNO` VARCHAR(50))  BEGIN
	SELECT FNAME
			,LNAME
	FROM STUDENT
	WHERE STUD_NO = P_STUDNO;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SELECT_UACS_TABLE` ()  BEGIN
	SELECT UACS_CODE
			,OLD_CODE
			,FUND_TYPE
			,IFNULL(INCOME_TYPE,'N/A') AS 'INCOME_TYPE'
			,`DESC`
			,IS_ACTIVE
	FROM uacs;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_SET_CASHIER_EMAIL` (IN `P_EMAIL` VARCHAR(50), IN `P_PASS` VARCHAR(50))  BEGIN 
	INSERT INTO email_config(CASHIER_EMAIL, CASHIER_PASS, DATE_ADDED, DATE_UPDATED, IS_ACTIVE)
	VALUES(P_EMAIL
			,P_PASS
			,CURRENT_TIMESTAMP
			,CURRENT_TIMESTAMP
			,1);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_UPDATE_FUND_TYPE` (IN `P_FNDTYPE_ORIG` VARCHAR(50), IN `P_FNDTYPE_UPD` VARCHAR(50), IN `P_FNDCODE` VARCHAR(50))  BEGIN
	UPDATE FUND
	SET FUND_TYPE = UPPER(P_FNDTYPE_UPD)
		,FUND_CODE = UPPER(P_FNDCODE)
	WHERE UPPER(FUND_TYPE) = UPPER(P_FNDTYPE_ORIG)
		AND IS_ACTIVE = 1;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_UPDATE_INC_TYPE` (IN `P_INCTYPE_ORIG` VARCHAR(50), IN `P_INCTYPE_UPD` VARCHAR(50))  BEGIN
	UPDATE INCOME
	SET INCOME_TYPE = UPPER(P_INCTYPE_UPD)
	WHERE UPPER(INCOME_TYPE) = UPPER(P_INCTYPE_ORIG)
		AND IS_ACTIVE = 1;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_UPDATE_SCHED_DATE` (IN `P_NEWDATE` DATETIME, IN `P_GROUPID` VARCHAR(50))  BEGIN 
	UPDATE DEPOSIT
	SET DATE_SCHEDULED = P_NEWDATE
	WHERE GROUP_ID = P_GROUPID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_UPDATE_STATUS_UACS` (IN `CODE` VARCHAR(50), IN `STATUS` TINYINT)  BEGIN
	UPDATE UACS
	SET IS_ACTIVE = `STATUS`
	WHERE UACS_CODE = `CODE`;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_UPDATE_UACS_TABLE` (IN `PID` VARCHAR(50), IN `P_OLD_CODE` VARCHAR(50), IN `P_NEW_CODE` VARCHAR(50), IN `P_FND_TYPE` VARCHAR(50), IN `P_INC_TYPE` VARCHAR(50), IN `P_DESC_NAME` VARCHAR(50))  BEGIN
	IF P_INC_TYPE = 'N/A' THEN
		SET P_INC_TYPE = NULL;
	END IF;
	UPDATE UACS
	SET UACS_CODE = P_NEW_CODE
		,OLD_CODE = P_OLD_CODE
		,FUND_TYPE = P_FND_TYPE
		,INCOME_TYPE = P_INC_TYPE
		,`DESC` = P_DESC_NAME
		,LAST_UPDATED = NOW()
	WHERE UACS_CODE = PID
		AND IS_ACTIVE = 1;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_UPDATE_USER_DATA` (IN `P_ID` INT, IN `P_FNAME` VARCHAR(50), IN `P_MNAME` VARCHAR(50), IN `P_LNAME` VARCHAR(50), IN `P_ROLE` VARCHAR(50))  BEGIN
	UPDATE `USER`
	SET FNAME = P_FNAME
		,MNAME = P_MNAME
		,LNAME = P_LNAME
		,ROLE_ID = IF(UPPER(P_ROLE) = 'ADMIN', 1, 2)
	WHERE USER_ID = P_ID
		AND IS_ACTIVE = 1;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `collection`
--

CREATE TABLE `collection` (
  `OR_NUM` varchar(50) NOT NULL,
  `ASSESSED` decimal(10,2) DEFAULT NULL,
  `COLLECTED` decimal(10,2) DEFAULT NULL,
  `STUD_NO` varchar(50) DEFAULT NULL,
  `CLIENT_NAME` varchar(100) DEFAULT NULL,
  `EDUC_LEVEL` varchar(50) DEFAULT NULL,
  `TRANS_DATE` datetime NOT NULL,
  `STATUS` varchar(50) DEFAULT NULL,
  `USER_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `collection`
--

INSERT INTO `collection` (`OR_NUM`, `ASSESSED`, `COLLECTED`, `STUD_NO`, `CLIENT_NAME`, `EDUC_LEVEL`, `TRANS_DATE`, `STATUS`, `USER_ID`) VALUES
('00882510', '2500.00', '2500.00', '2017-00293-CM-0', 'SILLEZA, VAN ANTHONY', 'Bachelor\'s Degree', '2021-03-15 06:07:52', 'PENDING', 2),
('00882511', '13288.00', '13288.00', NULL, 'PUP, QUEZON CITY', 'SIS Payment', '2021-03-15 09:33:04', 'PENDING', 2),
('00882512', '1355.00', '1355.00', NULL, 'POTTER, NICOLAS', 'NON-STUDENT', '2021-03-18 06:57:15', 'PENDING', 2),
('00882513', '4250.00', '4250.00', NULL, 'SINOVAC', 'Company', '2021-03-18 07:12:35', 'PENDING', 2),
('00882514', '150.00', '150.00', '2018-00651-CM-1', 'PANLUBASAN, QUEEN KIMBERLY', 'Bachelor\'s Degree', '2021-03-18 07:23:17', 'PENDING', 2),
('00882515', '24000.00', '24000.00', NULL, 'MERALCO', 'Company', '2021-03-18 08:57:58', 'PENDING', 2);

-- --------------------------------------------------------

--
-- Table structure for table `collection_breakdown`
--

CREATE TABLE `collection_breakdown` (
  `ID` int(11) NOT NULL,
  `DESC` varchar(50) DEFAULT NULL,
  `AMT` decimal(10,2) DEFAULT NULL,
  `OR_NUM` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `collection_breakdown`
--

INSERT INTO `collection_breakdown` (`ID`, `DESC`, `AMT`, `OR_NUM`) VALUES
(121, 'GRADUATION FEE', '2500.00', '00882510'),
(122, 'PUBLICATION', '1355.00', '00882512'),
(123, 'LABORATORY FEE', '4250.00', '00882513'),
(124, 'CLEARANCE AND CERTIFICATION FEE', '150.00', '00882514'),
(125, 'ELECTRICITY', '24000.00', '00882515');

-- --------------------------------------------------------

--
-- Table structure for table `deposit`
--

CREATE TABLE `deposit` (
  `DEP_ID` int(11) NOT NULL,
  `OR_NUM` decimal(10,2) DEFAULT NULL,
  `GROUP_ID` varchar(50) DEFAULT NULL,
  `STATUS` varchar(50) DEFAULT NULL,
  `DATE_SCHEDULED` datetime DEFAULT NULL,
  `DATE_DEPOSITED` datetime DEFAULT NULL,
  `DATE_UPDATED` datetime DEFAULT NULL,
  `NOTES` varchar(255) DEFAULT NULL,
  `SLIP_NUM` varchar(50) DEFAULT NULL,
  `USER_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2020-10-23 13:08:21.395838'),
(2, 'auth', '0001_initial', '2020-10-23 13:08:24.348098'),
(3, 'admin', '0001_initial', '2020-10-23 13:08:34.937158'),
(4, 'admin', '0002_logentry_remove_auto_add', '2020-10-23 13:08:37.032877'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2020-10-23 13:08:37.101894'),
(6, 'contenttypes', '0002_remove_content_type_name', '2020-10-23 13:08:38.109687'),
(7, 'auth', '0002_alter_permission_name_max_length', '2020-10-23 13:08:39.501044'),
(8, 'auth', '0003_alter_user_email_max_length', '2020-10-23 13:08:39.774343'),
(9, 'auth', '0004_alter_user_username_opts', '2020-10-23 13:08:39.838624'),
(10, 'auth', '0005_alter_user_last_login_null', '2020-10-23 13:08:41.172865'),
(11, 'auth', '0006_require_contenttypes_0002', '2020-10-23 13:08:41.219498'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2020-10-23 13:08:41.287512'),
(13, 'auth', '0008_alter_user_username_max_length', '2020-10-23 13:08:41.458211'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2020-10-23 13:08:41.915864'),
(15, 'auth', '0010_alter_group_name_max_length', '2020-10-23 13:08:42.343708'),
(16, 'auth', '0011_update_proxy_permissions', '2020-10-23 13:08:42.439560'),
(17, 'sessions', '0001_initial', '2020-10-23 13:08:42.859024');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('12fhqz6eqnryz0yopi7jtapjpkq3d61a', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-02-21 10:27:58.479928'),
('39k9up6fa6b3ky71ya62ru7lskl34r8k', 'ZjUyZmJmMTZmODQ2MGE0MGUzMmY5N2YzOGQyZjM0YzczYjgxMDU1YTp7fQ==', '2020-12-11 01:51:09.586188'),
('3be5r7h41zdwu7lys01p189knsjqkg2x', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-03-21 05:24:05.453565'),
('3bnw7zbo5t2tg6vdq52du7rom1c42a30', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-02-22 17:01:13.071147'),
('5rwvfetzw6hb0r9a1wsln1xlw1g086md', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-02-21 00:14:40.378776'),
('c58i8zxkutqe3kz8y0mr3q0ptplc3m00', 'ZjUyZmJmMTZmODQ2MGE0MGUzMmY5N2YzOGQyZjM0YzczYjgxMDU1YTp7fQ==', '2020-12-10 21:08:56.555178'),
('czfl7dqma1as6r8cywh0efuf2tjn0ax7', 'MTZiMTZkMDkwOTlhZDVkYTViYTg1MzRlNDIxOTYwMDNmYTM4NmRlNDp7InVuYW1lIjoidmFuMDIxOSIsInJvbGUiOjF9', '2021-01-13 05:51:06.819861'),
('fsz5lqt1ndpeetlqr4kxk477yu35czn7', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-03-07 20:03:42.061979'),
('hl8x81y7a17w08hpk373t7ryoppby6sy', 'MTZiMTZkMDkwOTlhZDVkYTViYTg1MzRlNDIxOTYwMDNmYTM4NmRlNDp7InVuYW1lIjoidmFuMDIxOSIsInJvbGUiOjF9', '2021-03-20 21:09:28.542591'),
('isnahii2vupglitekl9z42zd80dy7krb', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-01-01 02:02:04.737300'),
('istn575r9cmjpomrvv4dbjxl9lc5t7yr', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-03-08 08:27:25.905790'),
('j4olfvzo098u5x2ze7h06d5wtnoavfgp', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-03-31 20:45:46.171191'),
('m3o0vsbv45jh089vh3gydyu169mdtkvt', 'MTZiMTZkMDkwOTlhZDVkYTViYTg1MzRlNDIxOTYwMDNmYTM4NmRlNDp7InVuYW1lIjoidmFuMDIxOSIsInJvbGUiOjF9', '2020-12-19 02:28:10.950441'),
('qycoimexdsv8dcmiiips55koinaydnhc', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-03-17 10:34:45.737135'),
('r6qsjc8o20p2wwqotrht8xztxjaro5za', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-02-11 03:52:58.041237'),
('sqws77hgwmturelx3u166l22cqn7y7ve', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-03-09 08:48:03.674253'),
('tn1hwwit49taeyck2qrk1uv67wwbnt3k', 'MTZiMTZkMDkwOTlhZDVkYTViYTg1MzRlNDIxOTYwMDNmYTM4NmRlNDp7InVuYW1lIjoidmFuMDIxOSIsInJvbGUiOjF9', '2021-03-21 01:47:49.164429'),
('vav52xes9rdnnyoqfei0qzxzeso757ti', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-02-21 09:34:23.696775'),
('vvds0afcod9fkn9kkg4esdk2dnsxx64b', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-03-21 06:29:43.803693'),
('xi0r3zd813q750oolxtp2rzvves1i9aa', 'N2RiNmI1ZTcyNmE5NDVjOTJjNzYxYzI3YzVlMzg1MDgzMDE1NWJlNzp7InVuYW1lIjoibWVncyIsInJvbGUiOjJ9', '2021-02-09 20:28:38.729315');

-- --------------------------------------------------------

--
-- Table structure for table `email_config`
--

CREATE TABLE `email_config` (
  `EMAIL_ID` int(11) NOT NULL,
  `CASHIER_EMAIL` varchar(50) DEFAULT NULL,
  `CASHIER_PASS` varchar(50) DEFAULT NULL,
  `DATE_ADDED` datetime DEFAULT NULL,
  `DATE_UPDATED` datetime DEFAULT NULL,
  `IS_ACTIVE` tinyint(4) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `email_config`
--

INSERT INTO `email_config` (`EMAIL_ID`, `CASHIER_EMAIL`, `CASHIER_PASS`, `DATE_ADDED`, `DATE_UPDATED`, `IS_ACTIVE`) VALUES
(1, 'van.silleza@gmail.com', 'evohelmet09@', '2021-03-11 07:34:14', '2021-03-11 07:34:14', 1);

-- --------------------------------------------------------

--
-- Table structure for table `fund`
--

CREATE TABLE `fund` (
  `FUND_TYPE` varchar(50) NOT NULL,
  `FUND_CODE` varchar(50) NOT NULL,
  `DATE_ADDED` datetime DEFAULT NULL,
  `IS_ACTIVE` tinyint(4) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `fund`
--

INSERT INTO `fund` (`FUND_TYPE`, `FUND_CODE`, `DATE_ADDED`, `IS_ACTIVE`) VALUES
('NEW FUND TYPE', '12345', '2021-03-07 13:23:02', 0),
('NEW FUND TYPPE', '846', '2021-02-16 18:55:25', 0),
('NEW INC TYPE', '1238293', '2021-01-06 20:28:31', 0),
('REGULAR TRUST FUND', '5 02 06 441 (164)', '2020-12-30 02:05:20', 1),
('SPECIAL TRUST FUND', '05 2 06 441 (164)', '2020-12-30 02:03:44', 1);

-- --------------------------------------------------------

--
-- Table structure for table `income`
--

CREATE TABLE `income` (
  `INCOME_TYPE` varchar(50) NOT NULL,
  `DATE_ADDED` datetime DEFAULT NULL,
  `IS_ACTIVE` tinyint(4) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `income`
--

INSERT INTO `income` (`INCOME_TYPE`, `DATE_ADDED`, `IS_ACTIVE`) VALUES
('BUSINESS INCOME', '2020-12-30 02:16:56', 1),
('SERVICE INCOME', '2020-12-30 02:16:25', 1);

-- --------------------------------------------------------

--
-- Table structure for table `or_set`
--

CREATE TABLE `or_set` (
  `ID` int(11) NOT NULL,
  `OR_NUM_START` varchar(50) NOT NULL,
  `OR_NUM_END` varchar(50) NOT NULL,
  `DATE_ADDED` datetime DEFAULT NULL,
  `ORIG_COUNT` int(11) DEFAULT NULL,
  `CURR_COUNT` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `or_set`
--

INSERT INTO `or_set` (`ID`, `OR_NUM_START`, `OR_NUM_END`, `DATE_ADDED`, `ORIG_COUNT`, `CURR_COUNT`) VALUES
(4, '00882510', '00882610', '2021-03-15 05:51:48', 101, 95);

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `ROLE_ID` int(11) NOT NULL,
  `ROLE_NAME` varchar(50) NOT NULL,
  `DATE_CREATED` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`ROLE_ID`, `ROLE_NAME`, `DATE_CREATED`) VALUES
(1, 'ADMIN', '2020-11-18 04:38:32'),
(2, 'CASHIER', '2020-11-18 04:39:18');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `STUD_NO` varchar(50) NOT NULL,
  `FNAME` varchar(50) NOT NULL,
  `MNAME` varchar(50) DEFAULT NULL,
  `LNAME` varchar(50) NOT NULL,
  `COURSE` varchar(50) NOT NULL,
  `YR` int(11) NOT NULL,
  `SEC` int(11) NOT NULL,
  `IS_ACTIVE` tinyint(4) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`STUD_NO`, `FNAME`, `MNAME`, `LNAME`, `COURSE`, `YR`, `SEC`, `IS_ACTIVE`) VALUES
('2017-00007-CM-0', 'MARK LOURENZ', '', 'FLORES', 'BSIT', 4, 1, 1),
('2017-00011-CM-0', 'ALEXANDRA', '', 'ERMITA', 'BSIT', 4, 1, 1),
('2017-00034-CM-0', 'ROSANO', '', 'SORIA', 'BSIT', 4, 1, 1),
('2017-00040-CM-0', 'CHANTAL', '', 'DIVERSON', 'BSIT', 4, 1, 1),
('2017-00043-CM-0', 'MARIZ', '', 'MONTEMAYOR', 'BSIT', 4, 1, 1),
('2017-00045-CM-0', 'RODEL', '', 'DUTERTE', 'BSIT', 4, 1, 1),
('2017-00099-CM-0', 'DANIEL', '', 'JIMENEZ', 'BSIT', 4, 1, 1),
('2017-00100-CM-0', 'GLENN', '', 'BALIZA', 'BSIT', 4, 1, 1),
('2017-00107-CM-0', 'SHEENA MARIE', '', 'MANJARES', 'BSIT', 4, 1, 1),
('2017-00110-CM-0', 'RALPH LAWRENCE', '', 'TARLAC', 'BSIT', 4, 1, 1),
('2017-00117-CM-0', 'JOHN CHRISTOPHER', '', 'MORALES', 'BSIT', 4, 1, 1),
('2017-00188-CM-0', 'JAYSON', '', 'GUEVARRA', 'BSIT', 4, 1, 1),
('2017-00257-CM-0', 'RICHARD', '', 'VILLACORTA', 'BSIT', 4, 1, 1),
('2017-00273-CM-0', 'DAISY', '', 'BRILLO', 'BSIT', 4, 1, 1),
('2017-00275-CM-0', 'JOHN PHILIP', '', 'VILLANUEVA', 'BSIT', 4, 1, 1),
('2017-00288-CM-0', 'JOSHUA VENELL', '', 'LAXAMANA', 'BSIT', 4, 1, 1),
('2017-00293-CM-0', 'VAN ANTHONY', '', 'SILLEZA', 'BSIT', 4, 1, 1),
('2017-00297-CM-0', 'JELLIE MAE', '', 'ORTIZ', 'BSIT', 4, 1, 1),
('2017-00299-CM-0', 'EARL JOHN', '', 'ESPAÑOLA', 'BSIT', 4, 1, 1),
('2017-00306-CM-0', 'JESSIE JAMES', '', 'MERCURIO', 'BSIT', 4, 1, 1),
('2017-00308-CM-0', 'MARK KENNEDY', '', 'ASILAN', 'BSIT', 4, 1, 1),
('2017-00331-CM-0', 'ROMUALDO', '', 'LAGON', 'BSIT', 4, 1, 1),
('2017-00336-CM-0', 'ANEL THOM', '', 'MACALLA', 'BSIT', 4, 1, 1),
('2017-00346-CM-0', 'JONATHAN', '', 'CAÑOLAS', 'BSIT', 4, 1, 1),
('2017-00389-CM-1', 'MARINEL', '', 'CANTUJA', 'BSIT', 4, 1, 1),
('2017-00403-CM-0', 'LEAH', '', 'MACALIPAY', 'BSIT', 4, 1, 1),
('2018-00651-CM-1', 'QUEEN KIMBERLY', 'PENEDILLA', 'PANLUBASAN', 'BSIT', 4, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `uacs`
--

CREATE TABLE `uacs` (
  `UACS_CODE` varchar(50) NOT NULL,
  `OLD_CODE` varchar(50) DEFAULT NULL,
  `FUND_TYPE` varchar(50) DEFAULT NULL,
  `INCOME_TYPE` varchar(50) DEFAULT NULL,
  `DESC` varchar(50) NOT NULL,
  `DATE_ADDED` datetime DEFAULT NULL,
  `IS_ACTIVE` tinyint(4) DEFAULT 1,
  `LAST_UPDATED` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `uacs`
--

INSERT INTO `uacs` (`UACS_CODE`, `OLD_CODE`, `FUND_TYPE`, `INCOME_TYPE`, `DESC`, `DATE_ADDED`, `IS_ACTIVE`, `LAST_UPDATED`) VALUES
('0821939902', 'N/A', 'REGULAR TRUST FUND', 'SERVICE INCOME', 'NEW PAYMENT New', '2021-02-16 18:54:18', 0, '2021-02-16 18:54:55'),
('083 393 839739', 'N/A', 'REGULAR TRUST FUND', 'SERVICE INCOME', 'NEW FEE', '2021-03-07 13:22:27', 0, NULL),
('12444', 'N/A', 'REGULAR TRUST FUND', 'SERVICE INCOME', 'PENALTIES', '2021-03-06 23:21:38', 0, '2021-03-06 23:24:22'),
('2 99 99 990 00 00000', '439', 'SPECIAL TRUST FUND', NULL, 'OTHER PAYABLE', '2020-12-30 03:02:58', 1, '2021-01-06 17:27:25'),
('4 02 01 040 00 00000', '613', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'CLEARANCE AND CERTIFICATION FEE', '2020-12-30 02:23:46', 1, '2021-01-05 01:03:21'),
('4 02 01 140 00 00000', '629', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'FINES AND PENALTIES', '2020-12-30 02:26:33', 1, NULL),
('4 02 01 990 99 00001', '628A', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'ID', '2020-12-30 02:27:31', 1, '2021-01-05 19:55:11'),
('4 02 01 990 99 00002', '628B', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'ENTRANCE FEES', '2020-12-30 02:28:02', 1, '2021-01-03 03:17:41'),
('4 02 01 990 99 00003', '628b1', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'ENGLISH TEST', '2020-12-30 02:28:36', 1, NULL),
('4 02 01 990 99 00004', '628C', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'MODULE', '2020-12-30 02:28:58', 1, NULL),
('4 02 01 990 99 00005', '628C1', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'NSTP MODULE', '2020-12-30 02:29:32', 1, NULL),
('4 02 01 990 99 00006', '628C2', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'GRADUATE FORUM', '2020-12-30 02:30:00', 1, NULL),
('4 02 01 990 99 00007', '628C5', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'PUBLICATION', '2020-12-30 02:30:20', 1, NULL),
('4 02 01 990 99 00008', '628D', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'INCOME FROM IT', '2020-12-30 02:30:56', 1, NULL),
('4 02 01 990 99 00009', '628E', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'REGISTRATION', '2020-12-30 02:31:20', 1, NULL),
('4 02 01 990 99 00020', '628J', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'PERMIT FEE', '2020-12-30 02:31:43', 1, NULL),
('4 02 01 990 99 00021', '628K1', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'DUPLICATE', '2020-12-30 02:32:07', 1, NULL),
('4 02 01 990 99 00022', '628K2', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'HD', '2020-12-30 02:32:24', 1, NULL),
('4 02 01 990 99 00023', '628K3', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'COMPLETION', '2020-12-30 02:32:52', 1, '2021-01-03 02:58:57'),
('4 02 01 990 99 00024', '628K4', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'READMISSION', '2020-12-30 02:33:14', 1, NULL),
('4 02 01 990 99 00025', '628K5', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'RETRIEVAL', '2020-12-30 02:33:31', 1, NULL),
('4 02 01 990 99 00026', '628K6', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'HANDBOOK', '2020-12-30 02:33:48', 1, NULL),
('4 02 01 990 99 00027', '628K7', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'SCANNABLE', '2020-12-30 02:34:05', 1, NULL),
('4 02 01 990 99 00028', '628K8', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'CHANGE SUBJECT', '2020-12-30 02:34:25', 1, NULL),
('4 02 01 990 99 00029', '628K9', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'ACCREDITATION', '2020-12-30 02:34:44', 1, NULL),
('4 02 01 990 99 00030', '628K10', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'EVALUATION', '2020-12-30 02:35:13', 1, NULL),
('4 02 01 990 99 00031', '628K11', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'GUIDANCE FEE', '2020-12-30 02:35:44', 1, NULL),
('4 02 01 990 99 00032', '628K12', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'PSYCHOLOGICAL EXAM', '2020-12-30 02:36:07', 1, NULL),
('4 02 01 990 99 00033', '628L', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'DEVELOPMENTAL FEE', '2020-12-30 02:36:39', 1, NULL),
('4 02 01 990 99 00034', '628L1', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'SIS', '2020-12-30 02:36:55', 1, NULL),
('4 02 01 990 99 00035', '628L2', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'ITD', '2020-12-30 02:37:12', 1, NULL),
('4 02 01 990 99 00036', '628M', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'AUTHENTICATION FEE', '2020-12-30 02:37:37', 1, NULL),
('4 02 01 990 99 00037', '628N', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'SPORTS DEVELOPMENT', '2020-12-30 02:38:21', 1, NULL),
('4 02 01 990 99 00038', '628P', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'DEPOSIT', '2020-12-30 02:38:41', 1, NULL),
('4 02 01 990 99 00039', '628O', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'PUP SPONSOR SEMINAR', '2020-12-30 02:39:08', 1, NULL),
('4 02 01 990 99 00041', '628S', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'ENERGY FEE', '2020-12-30 02:39:31', 1, NULL),
('4 02 01 990 99 00042', '628T', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'TUTORIAL', '2020-12-30 02:39:51', 1, NULL),
('4 02 01 990 99 00043', '628U', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'MEMORABILIA', '2020-12-30 02:41:19', 1, NULL),
('4 02 01 990 99 00044', '628V', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'VERIFICATION', '2020-12-30 02:41:36', 1, NULL),
('4 02 01 990 99 00048', '628D2', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'STATISTICAL CONSULTANCY', '2020-12-30 02:42:15', 1, NULL),
('4 02 01 990 99 00049', '628D1', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'MASTER STATISTICAL CONSULTANCY', '2020-12-30 02:42:52', 1, NULL),
('4 02 01 990 99 00050', '628C3', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'RESEARCH JOURNAL', '2020-12-30 02:44:34', 1, NULL),
('4 02 01 990 99 00051', '628X', 'SPECIAL TRUST FUND', 'SERVICE INCOME', 'NSTP PROGRAM', '2020-12-30 02:44:54', 1, NULL),
('4 02 02 010 01 00000', '644', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'TUITION FEES', '2020-12-30 02:45:51', 1, NULL),
('4 02 02 010 01 00001', '644A', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'TUITION FEES NSTP', '2020-12-30 02:46:08', 1, NULL),
('4 02 02 010 01 00002', '644C', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'TUITION FEES DOLLAR', '2020-12-30 02:46:23', 1, NULL),
('4 02 02 010 99 00001', '612', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'CULTURAL FEES', '2020-12-30 02:47:34', 1, NULL),
('4 02 02 010 99 00002', '612A', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'ATHLETIC FEES', '2020-12-30 02:47:53', 1, NULL),
('4 02 02 010 99 00003', '612B', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'ATHLETIC DEVELOPMENT FEES', '2020-12-30 02:48:18', 1, NULL),
('4 02 02 010 99 00004', '615', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'DIPLOMA', '2020-12-30 02:48:36', 1, NULL),
('4 02 02 010 99 00005', '615A', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'GRADUATION FEE', '2020-12-30 02:48:59', 1, NULL),
('4 02 02 010 99 00006', '618', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'LIBRARY FEES', '2020-12-30 02:49:42', 1, NULL),
('4 02 02 010 99 00007', '619A', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'MEDICAL, DENTAL', '2020-12-30 02:50:11', 1, NULL),
('4 02 02 010 99 00008', '619', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'LABORATORY FEE', '2020-12-30 02:50:48', 1, NULL),
('4 02 02 010 99 00009', '624', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'TRANSCRIPT OF RECORD FEES', '2020-12-30 02:51:20', 1, NULL),
('4 02 02 010 99 00010', '624A', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'TRANSCRIPT OF RECORD FEES(SCANNED PHOTO)', '2020-12-30 02:51:55', 1, NULL),
('4 02 02 030 00 00000', '614', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'COMPREHENSIVE EXAMINATION FEE', '2020-12-30 02:53:04', 1, NULL),
('4 02 02 050 00 00000', '642', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'RENT INCOME/CANTEEN', '2020-12-30 02:53:59', 1, NULL),
('4 02 02 050 00 00001', '642', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'RENTAL', '2020-12-30 02:55:37', 1, NULL),
('4 02 02 050 00 00005', '642B3', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'ELECTRICITY', '2020-12-30 02:56:04', 1, NULL),
('4 02 02 050 00 00006', '642C', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'FACILITIES', '2020-12-30 02:56:28', 1, NULL),
('4 02 02 990 99 00004', '648K', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'BOOKS', '2020-12-30 02:57:42', 1, NULL),
('4 02 02 990 99 00005', '628D1', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'MEDICAL EXAM', '2020-12-30 02:58:37', 1, NULL),
('4 02 02 990 99 00006', '648E', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'PE UNIFORM', '2020-12-30 02:59:40', 1, NULL),
('4 02 02 990 99 00007', '648E4', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'SCHOOL UNIFORM', '2020-12-30 02:59:57', 1, NULL),
('4 02 02 990 99 00008', '648E4', 'SPECIAL TRUST FUND', 'BUSINESS INCOME', 'SCHOOL UNIFORM SENIOR HIGH', '2020-12-30 03:00:58', 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `USER_ID` int(11) NOT NULL,
  `FNAME` varchar(50) NOT NULL,
  `MNAME` varchar(50) DEFAULT NULL,
  `LNAME` varchar(50) NOT NULL,
  `UNAME` varchar(50) NOT NULL,
  `EMAIL` varchar(50) DEFAULT NULL,
  `PSWORD` varchar(50) NOT NULL,
  `DATE_ADDED` datetime NOT NULL,
  `ROLE_ID` int(11) DEFAULT NULL,
  `IS_ACTIVE` tinyint(4) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`USER_ID`, `FNAME`, `MNAME`, `LNAME`, `UNAME`, `EMAIL`, `PSWORD`, `DATE_ADDED`, `ROLE_ID`, `IS_ACTIVE`) VALUES
(1, 'Van Anthony', '', 'Silleza', 'van0219', 'van.silleza@gmail.com', '054eba9e024b4b0c4e7b5143ef573748', '2020-11-21 07:23:36', 1, 1),
(2, 'Merly', 'B', 'Gonzalbo', 'megs', NULL, '054eba9e024b4b0c4e7b5143ef573748', '2020-11-27 09:21:26', 2, 1),
(16, 'Van Anthony', '', 'Silleza', 'van1994', 'vasilleza@iskolarngbayan.pup.edu.ph', '5519ab0bd5416e69c69de03aeaa167e4', '2021-03-11 10:05:36', 2, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `collection`
--
ALTER TABLE `collection`
  ADD PRIMARY KEY (`OR_NUM`),
  ADD KEY `STUD_NO` (`STUD_NO`),
  ADD KEY `USER_ID` (`USER_ID`);

--
-- Indexes for table `collection_breakdown`
--
ALTER TABLE `collection_breakdown`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `OR_NUM` (`OR_NUM`);

--
-- Indexes for table `deposit`
--
ALTER TABLE `deposit`
  ADD PRIMARY KEY (`DEP_ID`),
  ADD KEY `USER_ID` (`USER_ID`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `email_config`
--
ALTER TABLE `email_config`
  ADD PRIMARY KEY (`EMAIL_ID`);

--
-- Indexes for table `fund`
--
ALTER TABLE `fund`
  ADD PRIMARY KEY (`FUND_TYPE`),
  ADD UNIQUE KEY `FUND_CODE` (`FUND_CODE`);

--
-- Indexes for table `income`
--
ALTER TABLE `income`
  ADD PRIMARY KEY (`INCOME_TYPE`);

--
-- Indexes for table `or_set`
--
ALTER TABLE `or_set`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `OR_NUM_START` (`OR_NUM_START`),
  ADD UNIQUE KEY `OR_NUM_END` (`OR_NUM_END`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`ROLE_ID`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`STUD_NO`);

--
-- Indexes for table `uacs`
--
ALTER TABLE `uacs`
  ADD PRIMARY KEY (`UACS_CODE`),
  ADD KEY `FUND_TYPE` (`FUND_TYPE`),
  ADD KEY `INCOME_TYPE` (`INCOME_TYPE`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`USER_ID`),
  ADD UNIQUE KEY `UNAME` (`UNAME`),
  ADD KEY `ROLE_ID` (`ROLE_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `collection_breakdown`
--
ALTER TABLE `collection_breakdown`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=126;

--
-- AUTO_INCREMENT for table `deposit`
--
ALTER TABLE `deposit`
  MODIFY `DEP_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=255;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `email_config`
--
ALTER TABLE `email_config`
  MODIFY `EMAIL_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `or_set`
--
ALTER TABLE `or_set`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `ROLE_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `USER_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `collection`
--
ALTER TABLE `collection`
  ADD CONSTRAINT `collection_ibfk_1` FOREIGN KEY (`STUD_NO`) REFERENCES `student` (`STUD_NO`),
  ADD CONSTRAINT `collection_ibfk_2` FOREIGN KEY (`USER_ID`) REFERENCES `user` (`USER_ID`);

--
-- Constraints for table `collection_breakdown`
--
ALTER TABLE `collection_breakdown`
  ADD CONSTRAINT `collection_breakdown_ibfk_1` FOREIGN KEY (`OR_NUM`) REFERENCES `collection` (`OR_NUM`);

--
-- Constraints for table `deposit`
--
ALTER TABLE `deposit`
  ADD CONSTRAINT `deposit_ibfk_1` FOREIGN KEY (`USER_ID`) REFERENCES `user` (`USER_ID`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `uacs`
--
ALTER TABLE `uacs`
  ADD CONSTRAINT `uacs_ibfk_1` FOREIGN KEY (`FUND_TYPE`) REFERENCES `fund` (`FUND_TYPE`),
  ADD CONSTRAINT `uacs_ibfk_2` FOREIGN KEY (`INCOME_TYPE`) REFERENCES `income` (`INCOME_TYPE`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`ROLE_ID`) REFERENCES `role` (`ROLE_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
