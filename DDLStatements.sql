CREATE TABLE Category (
	CategoryId INTEGER,
	Name TEXT,	
	PRIMARY KEY (CategoryId)
);

CREATE TABLE CategoryHierarchy (
	CategoryId INTEGER,
	ChildCategoryId INTEGER,	
	PRIMARY KEY (ChildCategoryId),
	FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
	FOREIGN KEY (ChildCategoryId) REFERENCES Category(CategoryId)
);


CREATE TABLE CategoryProduct (
	CategoryId INTEGER,
	ProductId INTEGER,	
	PRIMARY KEY (CategoryId, ProductId),
	FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId)
	FOREIGN KEY (ProductId) REFERENCES Product(ProductId)
);



CREATE TABLE Customer (
	CustomerId INTEGER,
	FirstName TEXT,
	LastName TEXT,
	Phone TEXT,
	Address TEXT,
	Email TEXT,
	Password TEXT,
	PRIMARY KEY (CustomerId)
);

CREATE TABLE OrderDetails (
	OrderId INTEGER,
	ProductId INTEGER,
	Quantity INTEGER,
	PRIMARY KEY (OrderId,ProductId),
	FOREIGN KEY (OrderId) REFERENCES OrderX(OrderId),
	FOREIGN KEY (ProductId) REFERENCES Product(ProductId)
);



CREATE TABLE OrderX (
	OrderId INTEGER,
	CustomerId Integer,
	OrderDate DATE,
	ShipmentDate DATE,
	PRIMARY KEY (OrderId),
	UNIQUE (CustomerId, OrderDate),
	FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
);



CREATE TABLE Product (
	ProductId INTEGER,
	Name TEXT,
	Description TEXT,
	PRIMARY KEY (ProductId)	
);
