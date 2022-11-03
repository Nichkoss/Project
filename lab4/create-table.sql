CREATE TABLE additional_passenger (
  idpassenger int NOT NULL AUTO_INCREMENT,
  firstname varchar(45) NOT NULL,
  lastname varchar(45) NOT NULL,
  birthdate date NOT NULL,
  pass_ser varchar(45) NOT NULL,
  pass_num varchar(45) NOT NULL,
  expirydate date NOT NULL,
  email varchar(45) DEFAULT NULL,
  PRIMARY KEY (idpassenger)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE user (
  iduser int NOT NULL AUTO_INCREMENT,
  email varchar(255) NOT NULL,
  password varchar(32) NOT NULL,
  creation_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  mgr tinyint NOT NULL DEFAULT '0',
  firstname varchar(45) NOT NULL,
  lastname varchar(45) NOT NULL,
  birthdate date NOT NULL,
  pass_ser varchar(45) NOT NULL,
  pass_num varchar(45) NOT NULL,
  expirydate date NOT NULL,
  PRIMARY KEY (iduser)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;



CREATE TABLE booking (
  idbooking int NOT NULL AUTO_INCREMENT,
  total_price double NOT NULL,
  userid int NOT NULL,
  PRIMARY KEY (idbooking),
  KEY fk_book_user1_idx (userid),
  CONSTRAINT fk_book_user1 FOREIGN KEY (userid) REFERENCES user (iduser)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE flight (
  idflight int NOT NULL AUTO_INCREMENT,
  city_from varchar(45) NOT NULL,
  city_to varchar(45) NOT NULL,
  airport_from varchar(45) NOT NULL,
  airport_to varchar(45) NOT NULL,
  max_sits int NOT NULL,
  flight_date date NOT NULL,
  PRIMARY KEY (idflight)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE sit (
  idsit int NOT NULL AUTO_INCREMENT,
  sitnumber int NOT NULL,
  available tinyint NOT NULL,
  price float NOT NULL,
  flightid int NOT NULL,
  PRIMARY KEY (idsit),
  KEY fk_sit_flight1_idx (flightid),
  CONSTRAINT fk_sit_flight1 FOREIGN KEY (flightid) REFERENCES flight (idflight)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE ticket (
  idticket int NOT NULL AUTO_INCREMENT,
  extra_lug int DEFAULT NULL,
  creation_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  sitid int NOT NULL,
  bookingid int NOT NULL,
  passengerid int DEFAULT NULL,
  PRIMARY KEY (idticket),
  KEY fk_ticket_sit1_idx (sitid),
  KEY fk_ticket_book1_idx (bookingid),
  KEY fk_ticket_passenger1_idx (passengerid),
  CONSTRAINT fk_ticket_book1 FOREIGN KEY (bookingid) REFERENCES booking (idbooking),
  CONSTRAINT fk_ticket_passenger1 FOREIGN KEY (passengerid) REFERENCES additional_passenger (idpassenger),
  CONSTRAINT fk_ticket_sit1 FOREIGN KEY (sitid) REFERENCES sit (idsit)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


