const Cart = require("../../models/cart.model")
const Product = require("../../models/product.model")
const Order = require("../../models/order.model")
const User =  require("../../models/user.model")

//[GET] /checkout
module.exports.index = async(req, res) => {
    const cartId = req.cookies.cartId
    const cart = await Cart.findOne({
        _id: cartId,
    });

    cart.totalPrice = 0;

    if(cart.products.length > 0){
        for(const item of cart.products){
            const product = await Product.findOne({
               _id: item.product_id     
            }).select("thumbnail title slug price discountPercentage")
            product.priceNew = (product.price * (100 - product.discountPercentage)/100).toFixed(0);
            item.productInfo = product;
            item.totalPrice = item.quantity * product.priceNew;
            cart.totalPrice += item.totalPrice; 
        }
    }
    
    
    res.render("client/pages/order/index", {
        pagetile: "Thanh toán sản phẩm",
        cartDetail: cart,
    });
}

//[POST] /checkout/order
module.exports.order = async(req, res) => {
    const cartId = req.cookies.cartId
    const infoUser = req.body;
    const userID = res.locals.infoUser.id;
    console.log(res.locals.infoUser.id);
    const orderInfo = {
        card_id: cartId,
        userInfo: infoUser,
        products:[],
        users:{},
    } 

    const cart = await Cart.findOne({
        _id: cartId,
    })

    for(const product of cart.products){
        const infoProduct = await Product.findOne({
            _id: product.product_id,
        });

        const objectProduct = {
            product_id: product.product_id,
            price: infoProduct.price,
            discountPercentage: infoProduct.discountPercentage,
            quantity: product.quantity,
        };
        orderInfo.products.push(objectProduct);
    }
    
    //--account user
    // const userAccount = await User.findOne({
    //     _id: userID,
    // })

    // const objectUser = {
    //     user_id: userAccount.id,
    //     email: userAccount.email,
    //     tokenUser: userAccount.tokenUser,
    // };
    // orderInfo.users.push(objectUser);

    const userAccount = await User.findOne({
        _id: userID,
    });
    orderInfo.users.email = userAccount.email;
    orderInfo.users.user_id = userAccount.id;

    const order = new Order(orderInfo)
    await order.save();
    
    await Cart.updateOne({
        _id: cartId,
    },{
        products: [],
    });
    
    res.redirect(`/checkout/success/${order.id}`)
}


module.exports.success = async (req,res) => {
    const order = await Order.findOne({
        _id: req.params.orderId
    });

    order.totalPrice = 0

    for (const item of order.products) {
        const infoProduct = await Product.findOne({
            _id: item.product_id
        });

        item.title = infoProduct.title;
        item.thumbnail = infoProduct.thumbnail;
        item.priceNew = (item.price * (100 - item.discountPercentage)/100).toFixed(0);
        item.totalPrice = item.priceNew * item.quantity;
        order.totalPrice += item.totalPrice;
        await Product.updateOne({
            _id: item.product_id
        },{
            stock: infoProduct.stock - item.quantity,
        });
    }


    res.render("client/pages/order/success",{
        pagetile: "Đặt hàng thành công",
        order: order
    });
}