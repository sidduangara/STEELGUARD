import { Router, type IRouter } from "express";
import healthRouter from "./health";
import steelguardRouter from "./steelguard";

const router: IRouter = Router();

router.use(healthRouter);
router.use(steelguardRouter);

export default router;
