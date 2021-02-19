db.createUser({
    user: 'root',
    pwd: 'password',
    roles: [
        {
            role: 'readWrite',
            db: 'ACMESky',
        },
    ],
});

db = new Mongo().getDB("ACMESky");

db.createCollection('interests');
