# Amazon FC Assignment

We will be mocking up the idea behind the Amazon's Robotic Fulfilment Center. Your program should at least have a CLI component. You could choose to use Arcade or PyQt5 for a GUI.

Topics:
- Classes and objects
- Creating an API
- Unit Testing

## Item Flow
### In
1. Shipment comes in
2. Products scanned onto trolly
3. Products taken off trolly and scanned into bins Shelf #, Compartment #

### Order-fulfilment station
1. Shelf with product sent to worker
2. Monitor shopwing compartment # and item image
3. Scan product out of shelf
4. Place item into bin
5. Bin sent to packaging

### Ship-out station
1. Display shipping box type on screen
2. Stamp barcode and send address
3. Conveyor belt sends to truck 
