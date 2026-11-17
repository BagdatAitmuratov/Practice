CREATE TABLE "player_progress" (
	"user_id" text,
	"game_id" integer,
	"completed" integer DEFAULT 0 NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "player_progress_pkey" PRIMARY KEY("user_id","game_id")
);
