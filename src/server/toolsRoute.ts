import express from 'express';
import { toolManager } from './toolManager';

export const toolsRouter = express.Router();

toolsRouter.get('/', (req, res) => {
  const tools = toolManager.getTools();
  res.json(tools);
});
