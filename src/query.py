


def query_regent_name(qs=""):
    results = db.session.query(regent).filter(regent.Geslachtsnaam == qs).all()
    #order_count = db.session.query(Order).join(Product).filter(Product.id == 2).count()
    #print(order_count)

    return results
