"use client";

import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { apiFetch, ApiError } from "@/lib/api-client";
import type { Membership, Paginated } from "@/lib/types";

export default function AdminMembersPage() {
  const queryClient = useQueryClient();
  const [error, setError] = useState("");
  const [signoffForm, setSignoffForm] = useState<Record<string, { amount_returned: string; reason: string }>>(
    {}
  );

  const { data } = useQuery({
    queryKey: ["admin-memberships"],
    queryFn: () => apiFetch<Paginated<Membership>>("/memberships/"),
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["admin-memberships"] });

  const activate = async (id: string) => {
    setError("");
    try {
      await apiFetch(`/memberships/${id}/activate/`, { method: "POST" });
      invalidate();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not activate");
    }
  };

  const signoff = async (id: string) => {
    setError("");
    const values = signoffForm[id] || { amount_returned: "0", reason: "" };
    try {
      await apiFetch(`/memberships/${id}/signoff/`, {
        method: "POST",
        body: { amount_returned: Number(values.amount_returned), reason: values.reason },
      });
      invalidate();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not process sign-off");
    }
  };

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Members</h1>
      {error && <p className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</p>}

      <div className="space-y-3">
        {data?.results.map((m) => (
          <div key={m.id} className="rounded-lg border bg-white p-4 text-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">
                  {m.tier.name} — {m.status}
                </p>
                <p className="text-xs text-gray-400">User: {m.user}</p>
                {m.renewed_through && <p className="text-gray-500">Renews through {m.renewed_through}</p>}
              </div>
              {m.status === "PENDING_PAYMENT" && (
                <button
                  onClick={() => activate(m.id)}
                  className="rounded bg-green-600 px-3 py-1 text-xs font-medium text-white hover:bg-green-700"
                >
                  Activate (fees collected)
                </button>
              )}
            </div>

            {m.status === "ACTIVE" && (
              <div className="mt-3 flex flex-wrap items-center gap-2 border-t pt-3">
                <input
                  placeholder="Amount returned"
                  type="number"
                  step="0.01"
                  value={signoffForm[m.id]?.amount_returned ?? ""}
                  onChange={(e) =>
                    setSignoffForm({
                      ...signoffForm,
                      [m.id]: {
                        amount_returned: e.target.value,
                        reason: signoffForm[m.id]?.reason || "",
                      },
                    })
                  }
                  className="w-32 rounded border px-2 py-1 text-xs"
                />
                <input
                  placeholder="Deduction reason (if less than deposit)"
                  value={signoffForm[m.id]?.reason ?? ""}
                  onChange={(e) =>
                    setSignoffForm({
                      ...signoffForm,
                      [m.id]: {
                        amount_returned: signoffForm[m.id]?.amount_returned || "0",
                        reason: e.target.value,
                      },
                    })
                  }
                  className="flex-1 rounded border px-2 py-1 text-xs"
                />
                <button
                  onClick={() => signoff(m.id)}
                  className="rounded bg-gray-700 px-3 py-1 text-xs font-medium text-white hover:bg-gray-800"
                >
                  Sign off
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
