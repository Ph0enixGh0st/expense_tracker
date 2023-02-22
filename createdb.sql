create table budget(
    tag varchar(255) primary key,
    daily_limit integer
);

create table category(
    tag varchar(255) primary key,
    is_base_expense boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount integer,
    created datetime,
    category_name integer,
    raw_text text,
    FOREIGN KEY(category_name) REFERENCES category(tag)
);

insert into category (tag, is_base_expense, aliases)
values
    ("groceries", true, "ration, food, grub, snacks, snack"),
    ("coffee", true, "espresso, starbucks, cappuccino, latte"),
    ("dinner", true, "lunch, brunch, breakfast, eat out"),
    ("restaurants", false, "cafe, bar, uber eats, dash, doordash, eats"),
    ("transport", true, "metro, sub, subway, underground, bus, tram, trolley"),
    ("gym", false, "sports, training, health"),
    ("medicine", false, "meds, drugs, pills")
    ("taxi", false, "cab, uber, lyft"),
    ("phone", true, "att, at&t, vodafone, etisalat, turk, turktelecom, verizon, t-mobile, mobile, cell, mob"),
    ("internet", true, "wifi, wi-fi, router"),
    ("subscriptions", false, "prem"),
    ("other", false, "others, misc, different, etc");

insert into budget(tag, daily_limit) values ('base', 150);