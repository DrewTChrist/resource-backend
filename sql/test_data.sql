/* admin */
INSERT INTO users (
    first_name, 
    last_name, 
    username, 
    password_hash, 
    disabled, 
    administrator
) VALUES (
    "admin", 
    "admin", 
    "admin", 
    "$2b$12$ta.KupNchm/CPN8Op9mY5.uai237aSMbc8jft3z..6zWiEOUb3f3e", --- "admin"
    false, 
    true
);

/* disabled user */
INSERT INTO users (
    first_name, 
    last_name, 
    username, 
    password_hash, 
    disabled, 
    administrator
) VALUES (
    "disabled", 
    "disabled", 
    "disabled", 
    "$2b$12$ta.KupNchm/CPN8Op9mY5.uai237aSMbc8jft3z..6zWiEOUb3f3e", --- "admin"
    true, 
    false
);

/* regular user */
INSERT INTO users (
    first_name, 
    last_name, 
    username, 
    password_hash, 
    disabled, 
    administrator
) VALUES (
    "user", 
    "user", 
    "user", 
    "$2b$12$ta.KupNchm/CPN8Op9mY5.uai237aSMbc8jft3z..6zWiEOUb3f3e", --- "admin"
    false, 
    false
);

COMMIT;
