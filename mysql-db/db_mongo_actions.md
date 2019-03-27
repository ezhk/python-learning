# MongoDB history

    > use users
    switched to db users
    >
    >
    > db.createUser({user:"admin", pwd:"1234",roles:["readWrite","dbAdmin"]})
    Successfully added user: { "user" : "admin", "roles" : [ "readWrite", "dbAdmin" ] }
    > db.users.insert({"name": "Tom", "age": 28, languages: ["english", "spanish"]})
    WriteResult({ "nInserted" : 1 })
    > db.users.find()
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "age" : 28, "languages" : [ "english", "spanish" ] }
    > db.users.insert({"company":{"name":"Microsoft","age": 25, languages: ["english", "spanish"]}})
    WriteResult({ "nInserted" : 1 })
    > db.users.find({"company.name": "Microsoft"})
    { "_id" : ObjectId("5c9b74ddc4264ce5c790dfa9"), "company" : { "name" : "Microsoft", "age" : 25, "languages" : [ "english", "spanish" ] } }
    > db.users.find ({age: {$lt : 30}})
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "age" : 28, "languages" : [ "english", "spanish" ] }
    > db.users.find ({age: {$gt : 30, $lt: 50}})
    > db.users.find ({age: {$ne : 22}})
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "age" : 28, "languages" : [ "english", "spanish" ] }
    { "_id" : ObjectId("5c9b74ddc4264ce5c790dfa9"), "company" : { "name" : "Microsoft", "age" : 25, "languages" : [ "english", "spanish" ] } }
    > db.users.find ({age: {$in : [22, 32]}})
    > db.users.find ({age: {$nin : [22, 32]}})
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "age" : 28, "languages" : [ "english", "spanish" ] }
    { "_id" : ObjectId("5c9b74ddc4264ce5c790dfa9"), "company" : { "name" : "Microsoft", "age" : 25, "languages" : [ "english", "spanish" ] } }
    > db.users.find ({languages: {$all : [ "english" ,   "spanish" ]}})
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "age" : 28, "languages" : [ "english", "spanish" ] }
    > db.users.find ({languages: {$all : [ "english" ]}})
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "age" : 28, "languages" : [ "english", "spanish" ] }
    > db.users.find ({$or : [{name: "Tom"}, {age: 22}]})
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "age" : 28, "languages" : [ "english", "spanish" ] }
    > db.users.find ({languages: {$size:2}})
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "age" : 28, "languages" : [ "english", "spanish" ] }
    > db.users.find ({company: {$exists:true}})
    { "_id" : ObjectId("5c9b74ddc4264ce5c790dfa9"), "company" : { "name" : "Microsoft", "age" : 25, "languages" : [ "english", "spanish" ] } }
    > db.users.find ({name: {$regex:"b"}})
    > db.users.find ({name: {$regex:"^M"}})
    > db.users.find ({name: {$regex:"^T"}})
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "age" : 28, "languages" : [ "english", "spanish" ] }
    > db.users.save({name: "Eugene", age : 29, languages: ["english", "german", "spanish"]})
    WriteResult({ "nInserted" : 1 })
    > db.users.find ()
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "age" : 28, "languages" : [ "english", "spanish" ] }
    { "_id" : ObjectId("5c9b74ddc4264ce5c790dfa9"), "company" : { "name" : "Microsoft", "age" : 25, "languages" : [ "english", "spanish" ] } }
    { "_id" : ObjectId("5c9b7593c4264ce5c790dfaa"), "name" : "Eugene", "age" : 29, "languages" : [ "english", "german", "spanish" ] }
    > db.users.update({name : "Eugene", age: 29}, {$set: {age : 30}})
    WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
    > db.users.find ()
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "age" : 28, "languages" : [ "english", "spanish" ] }
    { "_id" : ObjectId("5c9b74ddc4264ce5c790dfa9"), "company" : { "name" : "Microsoft", "age" : 25, "languages" : [ "english", "spanish" ] } }
    { "_id" : ObjectId("5c9b7593c4264ce5c790dfaa"), "name" : "Eugene", "age" : 30, "languages" : [ "english", "german", "spanish" ] }
    > db.users.update({name : "Tom"}, {$unset: {salary: 1}})
    WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 0 })
    > db.users.find ()
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "age" : 28, "languages" : [ "english", "spanish" ] }
    { "_id" : ObjectId("5c9b74ddc4264ce5c790dfa9"), "company" : { "name" : "Microsoft", "age" : 25, "languages" : [ "english", "spanish" ] } }
    { "_id" : ObjectId("5c9b7593c4264ce5c790dfaa"), "name" : "Eugene", "age" : 30, "languages" : [ "english", "german", "spanish" ] }
    > db.users.update({name : "Tom"}, {$unset: {salary: 1, age: 1}})
    WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
    > db.users.find ()
    { "_id" : ObjectId("5c9b74c6c4264ce5c790dfa8"), "name" : "Tom", "languages" : [ "english", "spanish" ] }
    { "_id" : ObjectId("5c9b74ddc4264ce5c790dfa9"), "company" : { "name" : "Microsoft", "age" : 25, "languages" : [ "english", "spanish" ] } }
    { "_id" : ObjectId("5c9b7593c4264ce5c790dfaa"), "name" : "Eugene", "age" : 30, "languages" : [ "english", "german", "spanish" ] }

# Create dump

    # mongodump --collection users --db users --out 
    # ls -al dump/users/
    total 16
    drwxr-xr-x 2 root root 4096 Mar 27 16:11 .
    drwxr-xr-x 3 root root 4096 Mar 27 16:11 ..
    -rw-r--r-- 1 root root  309 Mar 27 16:11 users.bson
    -rw-r--r-- 1 root root  125 Mar 27 16:11 users.metadata.json


# Restore dump

    > use users
    switched to db users
    > db.dropDatabase()
    { "dropped" : "users", "ok" : 1 }
    > 
    bye
    # mongorestore dump/
    2019-03-27T16:16:19.638+0300	preparing collections to restore from
    2019-03-27T16:16:19.639+0300	reading metadata for users.users from dump/users/users.metadata.json
    2019-03-27T16:16:19.645+0300	restoring users.users from dump/users/users.bson
    2019-03-27T16:16:19.654+0300	no indexes to restore
    2019-03-27T16:16:19.654+0300	finished restoring users.users (3 documents)
    2019-03-27T16:16:19.654+0300	done

    # mongo
    > use users
    switched to db users
    > show collections
    users

