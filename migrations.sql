CREATE table internships (
    id int auto_increment not null,
    digital_id int,
    org_name varchar(48),
    org_address varchar(48),
    org_website varchar(32),
    nature_of_work varchar(32),
    reporting_authority varchar(32) null,
    start_date date,
    end_date date,
    internship_mode varchar(32),
    stipend varchar(8),
    stipend_amount varchar(8) null,
    ppo varchar(8),
    internship_status varchar(16),
    offer_letter varchar(32) null,
    completion_letter varchar(32) null,
    constraint pk_internships primary key (id)
);

INSERT INTO internships (digital_id, org_name, org_address, org_website, nature_of_work, reporting_authority, start_date, end_date, internship_mode, stipend, stipend_amount, ppo, internship_status, offer_letter, completion_letter)
VALUES
    (1001, 'ABC Company', '123 Main St, City', 'www.abc.com', 'Software Development', 'John Doe', '2024-05-01', '2024-07-31', 'Remote', 'Yes', '2000', 'Yes', 'Pending', 'Offer_ABC.pdf', 'Completion_ABC.pdf'),
    (1002, 'XYZ Corporation', '456 Elm St, Town', 'www.xyzcorp.com', 'Marketing', 'Jane Smith', '2024-06-15', '2024-08-15', 'In-office', 'No', NULL, 'No', 'Accepted', NULL, NULL),
    (1003, '123 Industries', '789 Oak St, Village', 'www.123industries.com', 'Data Analysis', 'David Brown', '2024-07-01', '2024-09-30', 'Hybrid', 'Yes', '1500', 'No', 'Pending', 'Offer_123.pdf', NULL);


select * from internships;

