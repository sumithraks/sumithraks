"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";

const memberLinks = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/browse", label: "Browse" },
  { href: "/checkouts", label: "My Checkouts" },
  { href: "/reservations", label: "Reservations" },
  { href: "/membership", label: "Membership" },
  { href: "/notifications", label: "Notifications" },
  { href: "/settings", label: "Settings" },
];

const staffLinks = [
  { href: "/admin/inventory", label: "Inventory" },
  { href: "/admin/donations", label: "Donations" },
  { href: "/admin/checkouts", label: "Checkouts" },
  { href: "/admin/reservations", label: "Reservations" },
  { href: "/admin/billing", label: "Billing" },
  { href: "/admin/members", label: "Members" },
];

export function Nav() {
  const { user, logout } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  if (!user) return null;

  const links = pathname.startsWith("/admin") ? staffLinks : memberLinks;

  return (
    <header className="border-b bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <div className="flex items-center gap-6">
          <Link href="/dashboard" className="font-semibold text-blue-600">
            Toy Library
          </Link>
          <nav className="hidden gap-4 text-sm md:flex">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`hover:text-blue-600 ${
                  pathname === link.href ? "font-medium text-blue-600" : "text-gray-600"
                }`}
              >
                {link.label}
              </Link>
            ))}
            {user.is_staff && (
              <Link
                href="/admin/inventory"
                className={`hover:text-blue-600 ${
                  pathname.startsWith("/admin") ? "font-medium text-blue-600" : "text-gray-600"
                }`}
              >
                Staff Console
              </Link>
            )}
          </nav>
        </div>
        <div className="flex items-center gap-3 text-sm">
          <span className="text-gray-500">{user.email}</span>
          <button
            onClick={() => {
              logout();
              router.push("/login");
            }}
            className="rounded border px-3 py-1 text-gray-700 hover:bg-gray-50"
          >
            Log out
          </button>
        </div>
      </div>
    </header>
  );
}
