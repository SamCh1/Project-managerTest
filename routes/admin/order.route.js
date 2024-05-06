const express = require('express');
const router = express.Router();

const controller = require("../../controllers/admin/order.controllers")


router.get("/", controller.index);
router.get("/detail/:orderId", controller.detail);
router.patch("/detail/:orderId", controller.detailPatch);
router.get("/edit/:orderId", controller.edit);
module.exports = router;