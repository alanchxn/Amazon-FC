from typing import List, Dict

class Item:
    """Item class

    Attrs:
        product_name (str): The name of the product.
        product_number (int): The product's identification number.
        barcode (int): An integer barcode of the product.
        image (str): The picture of the product.

    """

    def __init__(self, product_name: str, product_number: int, barcode: int, image: str):
        self.name = product_name
        self.number = product_number
        self.barcode = barcode
        self.image = image


class Shelf:
    """Shelf class

    Attrs:
        all_shelves (List[]): A list containing all the shelves.
        shelf_number (int): An integer of the number of the shelf.
        product_nums (List[int]): A list of unique item identifications numbers.

    """

    all_shelves = []

    def __init__(self, shelf_number: int, product_nums: List[int]):
        self.number = shelf_number
        self.compartments = {}
        for item in product_nums:
            self.compartments[item] = {"Quantity": 0, "Items Stored": None}
        Shelf.all_shelves.append(self)


class Cart:
    """Cart/trolly class

    Attrs:
        items_stored: An empty list.
    """

    def __init__(self):
        self.items_stored = []

    def assign_cart(self, shelf: object):
        """Assign the cart object to a shelf object"""
        self.shelf = shelf

    def scan_onto_cart(self, items: List[object]):
        """Scan items onto the cart if the cart is assigned to a shelf
        Args:
            items: a list of item objects
        """
        if hasattr(self, "shelf"):
            items_added = []
            for item in items:
                if item.number in self.shelf.compartments.keys():
                    self.items_stored.append(item)
                    items_added.append(item)
            for item in items_added:
                items.remove(item)

    def scan_onto_shelf(self):
        """Scan items into compartments in the shelf, from the trolly"""
        if hasattr(self, "shelf"):
            items_added = []
            for item in self.items_stored:
                if self.shelf.compartments[item.number]["Items Stored"] is None:
                    self.shelf.compartments[item.number]["Items Stored"] = []
                self.shelf.compartments[item.number]["Items Stored"].append(
                    item)
                self.shelf.compartments[item.number]["Quantity"] += 1
                items_added.append(item)
            for item in items_added:
                self.items_stored.remove(item)


class Bin:
    """Bin class

    Attrs:
        all_bins: An empty list.
        order_number (int): An integer representing the order number.
        product_num_and_quantity (Dict[str, int]): A dictionary taking the product number and quantity.
        items_contained: An empty list.
    """

    all_bins = []

    def __init__(self, order_number: int, product_num_and_quantity: Dict[str, int]):
        """Create a bin object

        Args:
            order_number: the order number
            product_num_and_quantity: a dictionary with product numbers as key terms and the quantity of each product as the value
        """
        self.order_num = order_number
        self.products_needed = product_num_and_quantity
        self.items_contained = []
        Bin.all_bins.append(self)

    def scan_into_bin(self):
        """Scans items into the bin"""
        for item_num in self.products_needed.keys():
            for shelf in Shelf.all_shelves:
                for product, info in shelf.compartments.items():
                    if item_num == product:
                        while info["Quantity"] > 0 and self.products_needed[item_num] > 0:
                            self.items_contained.append(
                                info["Items Stored"][0])
                            info["Items Stored"].pop(0)
                            self.products_needed[item_num] -= 1
                            info["Quantity"] -= 1
                        if self.products_needed[item_num] == 0:
                            self.products_needed[item_num] = None
                        else:
                            # reserve items that are currently available but order will not be sent out for shipping until order fulfilled for the item
                            items_missing = self.products_needed[item_num]
                            print(
                                f"Order Fulfillment Invalid: {items_missing} more items of (product number: {product}) needed to complete order.")

        # remove products from order that are scanned into bin
        self.products_needed = {item_num: quantity for item_num,
                                quantity in self.products_needed.items() if quantity is not None}


class Package:
    """Package class

    Attrs:
        all_packages: An empty list.
        order_num (int): An integer of the order number.
        package_type (str): A string stating the type of package.
        items: An empty list.
        stamped: A boolean value.
    """

    all_packages = []

    def __init__(self, order_num: int, package_type: str):
        self.order_num = order_num
        self.type = package_type
        self.items = []
        self.stamped = False
        Package.all_packages.append(self)

    def pack_items(self):
        """Put items into the package object"""
        items_packaged = []
        for container in Bin.all_bins:
            if container.order_num == self.order_num:
                for item in container.items_contained:
                    if item.number not in container.products_needed.keys():
                        self.items.append(item)
                        items_packaged.append(item)
        for item in items_packaged:
            container.items_contained.remove(item)

    def send_to_truck(self, address: str):
        """Send package object to the conveyor belt to be taken to the truck
        Args:
            address: the address the package is being sent to
        """
        if len(self.items) != 0:
            for truck in Truck.all_trucks:
                if self.order_num in truck.orders.keys():
                    truck.orders[self.order_num] = self
                    self.address = address
                    self.stamped = True


class Truck:
    """Truck class

    all_trucks: An empty list.
    truck_number (int): An integer representing the truck number.
    order_list (List[]): A list of all the orders.
    orders: An empty dictionary.
    """

    all_trucks = []

    def __init__(self, truck_number: int, order_list: List):
        self.number = truck_number
        self.orders = {}
        for order in order_list:
            self.orders[order] = None
        Truck.all_trucks.append(self)


item1 = Item("Bag", 1, 11, "bag.png")
item2 = Item("Chair", 2, 22, "chair.png")
item3 = Item("Pillow", 3, 33, "pillow.png")
item4 = Item("Pillow", 3, 44, "pillow.png")
items = [item1, item2, item3, item4]

shelf1 = Shelf(1111, [1, 3])
# print(shelf1.compartments)

cart1 = Cart()

# won't do anything since cart not assigned to a shelf
cart1.scan_onto_cart(items)
# print(cart1.items_stored)
# print(items)

cart1.assign_cart(shelf1)

# items can now be scanned onto cart
cart1.scan_onto_cart(items)
# print(cart1.items_stored)
# print(items)

cart1.scan_onto_shelf()
# print(shelf1.compartments)
# print(cart1.items_stored)

bin1 = Bin(123, {1: 4, 3: 2})
# print(bin1.products_needed)
bin1.scan_into_bin()
# print(bin1.products_needed)
# print(bin1.items_contained)

package1 = Package(123, "box")
package1.pack_items()
# print(package1.items)
# print(bin1.items_contained)

truck1 = Truck(12, [123, 456])
# print(truck1.orders)

package1.send_to_truck("8101 Leslie Street")
# print(truck1.orders)
# print(truck1.orders[123].address)
