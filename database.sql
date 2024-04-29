
CREATE TABLE users(
    user_login VARCHAR(50) UNIQUE PRIMARY KEY,
    hashed_password VARCHAR(250) NOT NULL,
    user_status VARCHAR(10) DEFAULT 'client' CHECK (user_status IN ('admin', 'client'))
);

COMMENT ON table users IS 'Only for storing authentication data';

COMMENT ON COLUMN users.user_login IS 'Supposed to be an email address';
COMMENT ON COLUMN users.hashed_password IS 'Supposed to store only hashed passwords';
COMMENT ON COLUMN users.user_status IS 'All registered users have client status by default';

CREATE TABLE profiles(
    profile_id VARCHAR(50) UNIQUE PRIMARY KEY REFERENCES users (user_login),          -- profile will be created with the same
    registered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,    -- primary key as users
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    profile_type VARCHAR(10) DEFAULT 'individual' CHECK(profile_type IN ('individual', 'company'));
    surname VARCHAR(50),
    firstname VARCHAR(50),
    patronymic VARCHAR(50),
    birthdate date,
    phone VARCHAR(21), --+338 (800) 555 35-55

);

COMMENT ON TABLE profiles IS 'Each user must have their own profile';

COMMENT ON COLUMN profiles.registered_at IS 'Registration timestamp';
COMMENT ON COLUMN profiles.updated_at IS 'The profile update timestamp';
COMMENT ON COLUMN profiles.profile_type IS 'The profile can represent the interests of both individuals and legal entities';


CREATE TABLE requests(
    request_id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL REFERENCES users (user_login),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    request_title VARCHAR(250) NOT NULL,
    
)

