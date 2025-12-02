// Authentication functions for HTML version
// Simplified version - only user login, no admin

const DATA_KEY = "etax_data_store_v1";
const USER_SESSION_KEY = "etax_user_session";

// Default data structure
const DEFAULT_DATA = {
  accounts: [
    {
      id: "user-1",
      name: "Tử Xuân Chiến",
      email: "user1@etax.local",
      password: "123456",
      role: "user",
      mstList: ["00109202830"],
      phone: "0901 234 567",
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    },
  ],
  mstProfiles: {
    "00109202830": {
      mst: "00109202830",
      fullName: "TỬ XUÂN CHIẾN",
      email: "user1@etax.local",
      phone: "0901 234 567",
      address: "Số 123 Nguyễn Huệ, Quận 1, TP. Hồ Chí Minh",
    },
  },
};

// Helper functions
function readData() {
  if (typeof window === "undefined") {
    return DEFAULT_DATA;
  }

  const raw = window.localStorage.getItem(DATA_KEY);
  if (!raw) {
    window.localStorage.setItem(DATA_KEY, JSON.stringify(DEFAULT_DATA));
    return DEFAULT_DATA;
  }

  try {
    const parsed = JSON.parse(raw);
    return {
      accounts: parsed.accounts ?? DEFAULT_DATA.accounts,
      mstProfiles: parsed.mstProfiles ?? DEFAULT_DATA.mstProfiles,
    };
  } catch {
    window.localStorage.setItem(DATA_KEY, JSON.stringify(DEFAULT_DATA));
    return DEFAULT_DATA;
  }
}

function writeData(data) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(DATA_KEY, JSON.stringify(data));
}

// Login user by MST and password
export async function loginUserByMst(mst, password) {
  const data = readData();
  
  // Find account that has this MST in mstList
  const account = data.accounts.find(
    (acc) => acc.role === "user" && acc.mstList.includes(mst) && acc.password === password
  );

  if (!account) {
    return null;
  }

  // Store session
  if (typeof window !== "undefined") {
    const session = {
      mst: mst,
      name: account.name,
      accountId: account.id,
      loginTime: new Date().toISOString(),
    };
    window.localStorage.setItem(USER_SESSION_KEY, JSON.stringify(session));
  }

  return {
    mst: mst,
    name: account.name,
    accountId: account.id,
  };
}

// Get current user session
export function getUserSession() {
  if (typeof window === "undefined") {
    return null;
  }

  const raw = window.localStorage.getItem(USER_SESSION_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

// Get profile by MST
export function getProfile(mst) {
  const data = readData();
  return data.mstProfiles[mst] || null;
}

// Logout user
export function logoutUser() {
  if (typeof window !== "undefined") {
    window.localStorage.removeItem(USER_SESSION_KEY);
  }
}

// Check if user is authenticated
export function isAuthenticated() {
  const session = getUserSession();
  return session !== null;
}

