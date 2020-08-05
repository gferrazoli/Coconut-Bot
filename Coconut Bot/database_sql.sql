CREATE TABLE IF NOT EXISTS DiscordUser (
  discord_user_id BIGINT NOT NULL,
  PRIMARY KEY (discord_user_id));

CREATE TABLE IF NOT EXISTS DiscordUserVoiceSession (
  session_id SERIAL NOT NULL,
  discord_user_id BIGINT NOT NULL,
  voice_channel_id BIGINT NOT NULL,
  total_time_spent DOUBLE PRECISION NOT NULL,
  PRIMARY KEY (session_id),
  CONSTRAINT fk_Times_User
    FOREIGN KEY (Discord_user_id)
    REFERENCES DiscordUser (discord_user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
