import sqlite3
import datetime
import string, random

random.seed(521)

def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

conn = sqlite3.connect('onlineshop')
cur = conn.cursor()
cur.execute("delete from customer")
cur.execute("delete from category")
cur.execute("delete from categoryhierarchy")
cur.execute("delete from product")
cur.execute("delete from categoryproduct")
cur.execute("delete from orderdetails")
cur.execute("delete from orderx")


# create a tree with 2 levels and branching factor 3
branchingFactor=3
numberOfProducts=200
numberOfCategoriesWithProducts=30
minProductsInCategory=5
maxProductsInCategory=30
totalNumberOfCategories=39
numberOfCustomers=100
numberOfCustomersWhoMadeAnOrder=80
maxNumberOfOrdersOfCustomer=10
maxNumberOfProductsInAnOrder=10

main_categories=[(i,str(i)) for i in range(0,branchingFactor)]
cur.executemany('insert into category values (?,?)',main_categories)	
cur.executemany('insert into categoryhierarchy values (?,?)',[(x[0],None) for x in main_categories])	
#0,1,2

l1=[]
for c in main_categories:
	level1=[(branchingFactor*(1+c[0])+i,c[1]+str(i)) for i in range(0,branchingFactor)]
	level1hier=[(branchingFactor*(1+c[0])+i,c[0]) for i in range(0,branchingFactor)]		
	cur.executemany('insert into category values (?,?)',level1)	
	cur.executemany('insert into categoryhierarchy values (?,?)',level1hier)	
	l1.extend(level1)


for c in l1:	
	level2=[(branchingFactor*(1+c[0])+i,c[1]+str(i)) for i in range(0,branchingFactor)]
	level2hier=[(branchingFactor*(1+c[0])+i, c[0]) for i in range(0,branchingFactor)]	
	cur.executemany('insert into category values (?,?)',level2)	
	cur.executemany('insert into categoryhierarchy values (?,?)',level2hier)	


products=[(i,''.join(random.sample(string.ascii_lowercase, 3)), ''.join(random.sample(string.ascii_lowercase, 10))) for i in range(0,numberOfProducts)]
cur.executemany('insert into product values (?,?,?)', products)



# choose some random products and assign them to random categories, 
# total number of categories is 3^3+3^2+3 = 39, some categories have nothing assigned
productcat=[]
chosenproducts=set()

for i in random.sample(range(0,totalNumberOfCategories),numberOfCategoriesWithProducts): 
	prods=random.sample(range(0,numberOfProducts),random.randint(minProductsInCategory,maxProductsInCategory)) 
	productcat.extend((i,p) for p in prods)
	chosenproducts.update(prods)
cur.executemany('insert into categoryproduct values (?,?)', productcat)

customers=[(i,'customer'+str(i)+'_fn','customer'+str(i)+'_ln',i,'a','e','p') for i in range(0,100)]
cur.executemany('insert into customer values (?,?,?,?,?,?,?)',customers)	


# create some orders for some random number of random customers
oid=0
orders=[]
orderdetails=[]
chosenproducts=list(chosenproducts)
for i in random.sample(range(0,numberOfCustomers),numberOfCustomersWhoMadeAnOrder):
	for j in range(0,random.randint(0,maxNumberOfOrdersOfCustomer)):
		odate=random_date(datetime.datetime(2016,1,1,1,1), datetime.datetime(2017,1,1,1,1))
		sdate=odate+datetime.timedelta(days=random.randint(0,5)) if random.random()<0.9 else None # with 90% probability it is shipped
		orders.append((oid, i, odate, sdate))					
		orderedProducts=[chosenproducts[p] for p in random.sample(range(0,len(chosenproducts)),random.randint(1,maxNumberOfProductsInAnOrder))]		
		# quantity is between 1 and 5
		orderdetails.extend([(oid,k,random.randint(1,5)) for k in orderedProducts])
		oid=oid+1


cur.executemany('insert into orderx values (?,?,?,?)',orders)	
cur.executemany('insert into orderdetails values (?,?,?)',orderdetails)	

cur.close()
conn.commit()
conn.close()


