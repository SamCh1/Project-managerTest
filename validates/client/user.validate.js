const schema = require("../../helpers/validation-schema.helper");

//validate register
module.exports.registerPost = (req, res ,next) => {
    if(!req.body.fullName) {
        req.flash("error","Họ tên không được để trống!");
        res.redirect("back");
        return;
    }

    if(!req.body.email){
        req.flash("error","Email không được để trống!");
        res.redirect("back");
        return;
    }

    if(!schema.validate(req.body.password)){
        const inValid = schema.validate(req.body.password ,{ details: true });
        const errorMessage = inValid[0];
        req.flash("error", errorMessage.message);
        res.redirect("back");
        return;
    }

    next();
};

//validate login user account
module.exports.loginPost = (req, res, next) => {
    if(!req.body.email){
        req.flash("error", "Email không được để trống")
        res.redirect("back");
        return;
    }

    if(!req.body.password){
        req.flash("error", "Mật khẩu không được để trống")
        res.redirect("back");
        return;
    }

    next();
};

// validate user account forgot password
module.exports.forgotPasswordPost = (req, res, next) => {
    if(!req.body.email){
        req.flash("error", "Email không được để trống!")
        res.redirect("back");
        return;
    }

    next();
}


//validate user account reset password
module.exports.resetPassowrdPost = (req, res, next) => {
    if(!schema.validate(req.body.password)){
        const inValid = schema.validate(req.body.password ,{ details: true });
        const errorMessage = inValid[0];
        req.flash("error", "password: " + errorMessage.message);
        res.redirect("back");
        return;
    }
    if(!schema.validate(req.body.confirmPassword)){
        const inValid = schema.validate(req.body.confirmPassword ,{ details: true });
        const errorMessage = inValid[0];
        req.flash("error", "confirm Password: " + errorMessage.message);
        res.redirect("back");
        return;
    }
    if(req.body.password !== req.body.confirmPassword){
        req.flash("error","Xác nhận mật khẩu không khớp với mật khẩu trên!")
        res.redirect("back");
        return;
    }

    next();
}