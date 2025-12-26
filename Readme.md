# Custom HTTP Server in Python

This project implements a basic HTTP server from scratch using Python sockets.

## Features
- Handles multiple clients using threading
- Supports HTTP/1.1 request parsing
- Implements REST-style endpoints

## Supported Endpoints

### GET /
Returns a welcome message.

### GET /echo?message=hello
Echoes the provided query parameter.

### POST /data
Creates a new data entry.
Body must be valid JSON.

### GET /data
Returns all stored data.

### GET /data/:id
Returns a single item by index.

### PUT /data/:id
Replaces an existing item.

### DELETE /data/:id
Deletes an item by index.

## Notes
- Data is stored in memory and resets on restart
- Designed for learning purposes
