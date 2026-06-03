// Azure AD / Entra ID session helpers — full implementation added with NextAuth in step 2

export type UserRole = "marketer" | "reviewer" | "admin";

export interface UserSession {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  tenantId: string;
}

export function hasRole(session: UserSession, required: UserRole): boolean {
  const hierarchy: UserRole[] = ["marketer", "reviewer", "admin"];
  return hierarchy.indexOf(session.role) >= hierarchy.indexOf(required);
}
