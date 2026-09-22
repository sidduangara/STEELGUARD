import { Router, type IRouter } from "express";
import {
  AcknowledgeAlertParams,
  AcknowledgeAlertResponse,
  CreateWorkerBody,
  CreateWorkerResponse,
  DeleteWorkerParams,
  GetAlertsResponse,
  GetAnalyticsResponse,
  GetAuthoritiesResponse,
  GetDashboardResponse,
  GetEmergencyStatusResponse,
  GetPlantResponse,
  GetWorkerParams,
  GetWorkerResponse,
  GetWorkersQueryParams,
  GetWorkersResponse,
  ResetEmergencyShutdownResponse,
  TriggerEmergencyShutdownBody,
  TriggerEmergencyShutdownResponse,
  UpdateWorkerBody,
  UpdateWorkerParams,
  UpdateWorkerResponse,
} from "@workspace/api-zod";

type Worker = ReturnType<typeof GetWorkerResponse.parse>;
type Alert = {
  id: string;
  severity: string;
  title: string;
  description: string;
  workerId: string;
  zone: string;
  riskScore: number;
  timestamp: string;
  status: string;
  authorityNotified: boolean;
};

const router: IRouter = Router();

const zoneNames = [
  "Furnace A",
  "Furnace B",
  "Crane Area",
  "Conveyor Area",
  "Rolling Mill",
  "Storage Area",
  "Maintenance Area",
  "Restricted Zone",
];

const workerSeed = [
  ["Rajesh Kumar", "Furnace", "Furnace Operator"],
  ["Anita Sharma", "Rolling Mill", "Mill Technician"],
  ["Vikram Singh", "Crane Area", "Crane Operator"],
  ["Meena Patel", "Maintenance", "Maintenance Lead"],
  ["Arjun Nair", "Conveyor", "Line Inspector"],
  ["Kavya Reddy", "Storage", "Logistics Coordinator"],
  ["Suresh Yadav", "Furnace", "Process Engineer"],
  ["Divya Menon", "Safety", "Safety Observer"],
  ["Imran Khan", "Maintenance", "Electrical Technician"],
  ["Priya Das", "Rolling Mill", "Quality Inspector"],
] as const;

const initials = (name: string) =>
  name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

function makeWorker(index: number): Worker {
  const [name, department, role] = workerSeed[index % workerSeed.length];
  const zone = zoneNames[index % zoneNames.length];
  const temperature = 34 + ((index * 7) % 14);
  const humidity = 48 + ((index * 11) % 34);
  const gasLevel = 8 + ((index * 13) % 37);
  const fatigueScore = 2 + ((index * 3) % 8);
  const ppeCompliance = Math.max(62, 98 - ((index * 5) % 28));
  const workingHours = 5.2 + ((index * 17) % 40) / 10;
  const hazardDistance = 1.6 + ((index * 9) % 42) / 10;
  const previousIncidents = index % 6 === 0 ? 2 : index % 3 === 0 ? 1 : 0;
  const riskScore = Math.min(
    97,
    Math.round(
      temperature * 0.8 +
        fatigueScore * 4 +
        (100 - ppeCompliance) * 0.55 +
        gasLevel * 0.45 +
        (8 - Math.min(hazardDistance, 8)) * 2 +
        previousIncidents * 4 -
        32,
    ),
  );
  const riskLevel =
    riskScore >= 90
      ? "CRITICAL"
      : riskScore >= 75
        ? "HIGH"
        : riskScore >= 48
          ? "MEDIUM"
          : "LOW";
  const hazardType =
    riskScore >= 90
      ? "Multiple Hazards"
      : temperature >= 43
        ? "Heat Stress"
        : gasLevel >= 35
          ? "Gas Exposure"
          : ppeCompliance < 70
            ? "PPE Violation"
            : fatigueScore >= 8
              ? "Fatigue"
              : hazardDistance < 2.5
                ? "Equipment Hazard"
                : "Routine Monitoring";

  return {
    workerId: `W${String(1025 + index).padStart(4, "0")}`,
    name,
    initials: initials(name),
    department,
    role,
    shift: index % 3 === 0 ? "Night · 22:00–06:00" : index % 2 === 0 ? "Day · 06:00–14:00" : "Evening · 14:00–22:00",
    zone,
    temperature,
    humidity,
    gasLevel,
    fatigueScore,
    ppeCompliance,
    workingHours,
    hazardDistance,
    previousIncidents,
    equipmentStatus: index % 9 === 0 ? "Inspection due" : "Operational",
    riskScore,
    riskLevel,
    hazardType,
    status: riskScore >= 75 ? "Needs attention" : "On shift",
    recommendation:
      riskScore >= 75
        ? "Schedule a supervisor review and move the worker away from the highest-risk condition."
        : "Continue routine monitoring and scheduled break cadence.",
  };
}

let workers: Worker[] = Array.from({ length: 100 }, (_, index) =>
  makeWorker(index),
);

const alertSeed: Alert[] = [
  {
    id: "ALT-2048",
    severity: "CRITICAL",
    title: "Compound exposure detected",
    description: "High temperature, gas exposure, and fatigue crossed prototype thresholds.",
    workerId: "W1025",
    zone: "Furnace A",
    riskScore: 94,
    timestamp: "10:32:18",
    status: "ACTIVE",
    authorityNotified: true,
  },
  {
    id: "ALT-2047",
    severity: "HIGH",
    title: "Restricted-zone proximity",
    description: "Worker is within the prototype hazard-distance threshold.",
    workerId: "W1031",
    zone: "Restricted Zone",
    riskScore: 82,
    timestamp: "10:27:06",
    status: "ACTIVE",
    authorityNotified: true,
  },
  {
    id: "ALT-2046",
    severity: "MEDIUM",
    title: "PPE compliance below target",
    description: "PPE compliance is below the configurable prototype threshold.",
    workerId: "W1034",
    zone: "Rolling Mill",
    riskScore: 61,
    timestamp: "10:19:44",
    status: "ACKNOWLEDGED",
    authorityNotified: false,
  },
  {
    id: "ALT-2045",
    severity: "HIGH",
    title: "Heat stress trend rising",
    description: "Temperature and fatigue are trending upward across the shift.",
    workerId: "W1041",
    zone: "Furnace B",
    riskScore: 79,
    timestamp: "10:12:21",
    status: "ACTIVE",
    authorityNotified: true,
  },
];
let alerts = [...alertSeed];

const authorities = [
  {
    level: 1,
    role: "Shift Safety Officer",
    name: "A. Kulkarni",
    channel: "Control room console",
    status: "Ready",
    responseTime: "< 1 min",
  },
  {
    level: 2,
    role: "Plant Operations Lead",
    name: "S. Iyer",
    channel: "Simulated SMS",
    status: "Ready",
    responseTime: "< 2 min",
  },
  {
    level: 3,
    role: "EHS Manager",
    name: "N. Rao",
    channel: "Simulated email",
    status: "Ready",
    responseTime: "< 5 min",
  },
  {
    level: 4,
    role: "Plant Director",
    name: "M. Thomas",
    channel: "Executive escalation",
    status: "Standby",
    responseTime: "< 10 min",
  },
];

let emergencyStatus = {
  mode: "SIMULATION ONLY",
  state: "STANDBY",
  initiatedAt: "—",
  initiatedBy: "—",
  reason: "No simulated emergency active.",
  affectedZones: [] as string[],
  notificationsSent: 0,
  auditId: "AUD-READY",
};

const riskColor: Record<string, string> = {
  LOW: "#38c793",
  MEDIUM: "#e8a34c",
  HIGH: "#f15b62",
  CRITICAL: "#ff3d4f",
};

function dashboard() {
  const totalWorkers = workers.length;
  const highRiskWorkers = workers.filter(
    (worker) => worker.riskLevel === "HIGH" || worker.riskLevel === "CRITICAL",
  ).length;
  const averageRiskScore = Math.round(
    workers.reduce((sum, worker) => sum + worker.riskScore, 0) / totalWorkers,
  );
  const ppeCompliance = Math.round(
    workers.reduce((sum, worker) => sum + worker.ppeCompliance, 0) /
      totalWorkers,
  );
  const riskDistribution = ["LOW", "MEDIUM", "HIGH"].map((name) => ({
    name,
    value: workers.filter((worker) => worker.riskLevel === name).length,
    color: riskColor[name],
  }));
  const riskTrend = ["06:00", "07:00", "08:00", "09:00", "10:00", "Now"].map(
    (label, index) => ({
      label,
      score: Math.max(28, averageRiskScore - 10 + index * 2),
      alerts: Math.max(2, alerts.length - 2 + index),
    }),
  );

  return GetDashboardResponse.parse({
    totalWorkers,
    highRiskWorkers,
    activeAlerts: alerts.filter((alert) => alert.status === "ACTIVE").length,
    averageRiskScore,
    ppeCompliance,
    incidents: 12,
    riskDistribution,
    riskTrend,
    updatedAt: new Date().toISOString(),
  });
}

const plant = zoneNames.map((name, index) => ({
  id: `zone-${index + 1}`,
  name,
  workerCount: workers.filter((worker) => worker.zone === name).length,
  temperature: 36 + ((index * 4) % 10),
  hazardLevel: index === 0 || index === 7 ? "HIGH" : index % 3 === 0 ? "MEDIUM" : "LOW",
  equipmentStatus: index === 6 ? "Maintenance window" : "Operational",
  riskScore: index === 0 ? 84 : index === 7 ? 78 : 25 + index * 7,
}));

router.get("/dashboard", (_req, res) => {
  res.json(dashboard());
});

router.get("/workers", (req, res) => {
  const parsed = GetWorkersQueryParams.safeParse(req.query);
  if (!parsed.success) {
    res.status(400).json({ error: "Invalid worker filters." });
    return;
  }
  const { department, riskLevel, search } = parsed.data;
  const query = search?.toLowerCase();
  const result = workers.filter((worker) => {
    const matchesDepartment = !department || worker.department === department;
    const matchesRisk = !riskLevel || worker.riskLevel === riskLevel;
    const matchesSearch =
      !query ||
      worker.name.toLowerCase().includes(query) ||
      worker.workerId.toLowerCase().includes(query) ||
      worker.zone.toLowerCase().includes(query);
    return matchesDepartment && matchesRisk && matchesSearch;
  });
  res.json(GetWorkersResponse.parse(result));
});

router.post("/workers", (req, res) => {
  const parsed = CreateWorkerBody.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Worker fields are incomplete." });
    return;
  }
  if (workers.some((worker) => worker.workerId === parsed.data.workerId)) {
    res.status(409).json({ error: "Worker ID already exists." });
    return;
  }
  const name = parsed.data.name.trim();
  const worker = WorkerInputToWorker({
    ...parsed.data,
    name,
    initials: initials(name),
  });
  workers = [worker, ...workers];
  res.status(201).json(CreateWorkerResponse.parse(worker));
});

function WorkerInputToWorker(input: {
  workerId: string;
  name: string;
  initials: string;
  department: string;
  role: string;
  shift: string;
  zone: string;
}): Worker {
  return {
    ...input,
    temperature: 36,
    humidity: 58,
    gasLevel: 10,
    fatigueScore: 3,
    ppeCompliance: 100,
    workingHours: 0,
    hazardDistance: 8,
    previousIncidents: 0,
    equipmentStatus: "Operational",
    riskScore: 24,
    riskLevel: "LOW",
    hazardType: "Routine Monitoring",
    status: "On shift",
    recommendation: "Continue routine monitoring and scheduled break cadence.",
  };
}

router.get("/workers/:workerId", (req, res) => {
  const parsed = GetWorkerParams.safeParse(req.params);
  if (!parsed.success) {
    res.status(400).json({ error: "Invalid worker ID." });
    return;
  }
  const worker = workers.find((item) => item.workerId === parsed.data.workerId);
  if (!worker) {
    res.status(404).json({ error: "Worker not found." });
    return;
  }
  res.json(GetWorkerResponse.parse(worker));
});

router.put("/workers/:workerId", (req, res) => {
  const params = UpdateWorkerParams.safeParse(req.params);
  const body = UpdateWorkerBody.safeParse(req.body);
  if (!params.success || !body.success) {
    res.status(400).json({ error: "Invalid worker update." });
    return;
  }
  const worker = workers.find((item) => item.workerId === params.data.workerId);
  if (!worker) {
    res.status(404).json({ error: "Worker not found." });
    return;
  }
  Object.assign(worker, body.data);
  res.json(UpdateWorkerResponse.parse(worker));
});

router.delete("/workers/:workerId", (req, res) => {
  const parsed = DeleteWorkerParams.safeParse(req.params);
  if (!parsed.success) {
    res.status(400).json({ error: "Invalid worker ID." });
    return;
  }
  const before = workers.length;
  workers = workers.filter((item) => item.workerId !== parsed.data.workerId);
  if (before === workers.length) {
    res.status(404).json({ error: "Worker not found." });
    return;
  }
  res.status(204).send();
});

router.get("/alerts", (_req, res) => {
  res.json(GetAlertsResponse.parse(alerts));
});

router.post("/alerts/:alertId/acknowledge", (req, res) => {
  const parsed = AcknowledgeAlertParams.safeParse(req.params);
  if (!parsed.success) {
    res.status(400).json({ error: "Invalid alert ID." });
    return;
  }
  const alert = alerts.find((item) => item.id === parsed.data.alertId);
  if (!alert) {
    res.status(404).json({ error: "Alert not found." });
    return;
  }
  alert.status = "ACKNOWLEDGED";
  res.json(AcknowledgeAlertResponse.parse(alert));
});

router.get("/plant", (_req, res) => {
  res.json(GetPlantResponse.parse(plant));
});

router.get("/analytics", (_req, res) => {
  res.json(
    GetAnalyticsResponse.parse({
      departments: ["Furnace", "Rolling Mill", "Maintenance", "Safety", "Storage"].map(
        (department) => ({
          department,
          risk: Math.round(
            workers
              .filter((worker) => worker.department === department)
              .reduce((sum, worker) => sum + worker.riskScore, 0) /
              Math.max(
                1,
                workers.filter((worker) => worker.department === department).length,
              ),
          ),
          workers: workers.filter((worker) => worker.department === department)
            .length,
        }),
      ),
      hazards: [
        { name: "Heat Stress", count: 12, level: "HIGH", trend: "+8%" },
        { name: "Gas Exposure", count: 4, level: "CRITICAL", trend: "+2%" },
        { name: "PPE Violation", count: 18, level: "MEDIUM", trend: "-4%" },
        { name: "Fatigue", count: 9, level: "HIGH", trend: "+5%" },
      ],
      shifts: [
        { shift: "Day", risk: 39 },
        { shift: "Evening", risk: 48 },
        { shift: "Night", risk: 61 },
      ],
    }),
  );
});

router.get("/authorities", (_req, res) => {
  res.json(GetAuthoritiesResponse.parse(authorities));
});

router.get("/emergency/status", (_req, res) => {
  res.json(GetEmergencyStatusResponse.parse(emergencyStatus));
});

router.post("/emergency/shutdown", (req, res) => {
  const parsed = TriggerEmergencyShutdownBody.safeParse(req.body);
  if (!parsed.success || !parsed.data.confirmed) {
    res
      .status(400)
      .json({ error: "A confirmed reason is required to start the simulation." });
    return;
  }
  if (emergencyStatus.state === "ACTIVE") {
    res.status(409).json({ error: "A simulated shutdown is already active." });
    return;
  }
  emergencyStatus = {
    mode: "SIMULATION ONLY",
    state: "ACTIVE",
    initiatedAt: new Date().toISOString(),
    initiatedBy: parsed.data.initiatedBy,
    reason: parsed.data.reason,
    affectedZones: [...zoneNames],
    notificationsSent: authorities.length,
    auditId: `AUD-${Date.now().toString().slice(-8)}`,
  };
  res.json(TriggerEmergencyShutdownResponse.parse(emergencyStatus));
});

router.post("/emergency/reset", (_req, res) => {
  emergencyStatus = {
    mode: "SIMULATION ONLY",
    state: "STANDBY",
    initiatedAt: "—",
    initiatedBy: "—",
    reason: "No simulated emergency active.",
    affectedZones: [],
    notificationsSent: 0,
    auditId: `AUD-RESET-${Date.now().toString().slice(-6)}`,
  };
  res.json(ResetEmergencyShutdownResponse.parse(emergencyStatus));
});

export default router;