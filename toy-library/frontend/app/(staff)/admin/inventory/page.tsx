"use client";

import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { apiFetch, ApiError } from "@/lib/api-client";
import type { Paginated, Toy } from "@/lib/types";

const STATUSES = [
  "INTAKE",
  "AVAILABLE",
  "RESERVED",
  "CHECKED_OUT",
  "OVERDUE",
  "BROKEN",
  "UNDER_REPAIR",
  "RETIRED",
];

export default function AdminInventoryPage() {
  const queryClient = useQueryClient();
  const [statusFilter, setStatusFilter] = useState("");
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ model_name: "", make: "", min_age_years: "", description: "" });

  const { data } = useQuery({
    queryKey: ["admin-toys", statusFilter],
    queryFn: () => apiFetch<Paginated<Toy>>(`/toys/?${statusFilter ? `status=${statusFilter}` : ""}`),
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["admin-toys"] });

  const createToy = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      await apiFetch("/toys/", {
        method: "POST",
        body: { ...form, min_age_years: form.min_age_years ? Number(form.min_age_years) : null },
      });
      setForm({ model_name: "", make: "", min_age_years: "", description: "" });
      setShowForm(false);
      invalidate();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not create toy");
    }
  };

  const transition = async (toyId: string, newStatus: string) => {
    setError("");
    try {
      await apiFetch(`/toys/${toyId}/transition/`, {
        method: "POST",
        body: { new_status: newStatus, reason: `Manually set to ${newStatus}` },
      });
      invalidate();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Transition not allowed");
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Inventory</h1>
        <button
          onClick={() => setShowForm((s) => !s)}
          className="rounded bg-blue-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-blue-700"
        >
          {showForm ? "Cancel" : "Add toy"}
        </button>
      </div>

      {error && <p className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</p>}

      {showForm && (
        <form onSubmit={createToy} className="grid grid-cols-2 gap-3 rounded-lg border bg-white p-4">
          <input
            placeholder="Model name"
            required
            value={form.model_name}
            onChange={(e) => setForm({ ...form, model_name: e.target.value })}
            className="rounded border px-3 py-2 text-sm"
          />
          <input
            placeholder="Make"
            required
            value={form.make}
            onChange={(e) => setForm({ ...form, make: e.target.value })}
            className="rounded border px-3 py-2 text-sm"
          />
          <input
            placeholder="Min age (years)"
            type="number"
            value={form.min_age_years}
            onChange={(e) => setForm({ ...form, min_age_years: e.target.value })}
            className="rounded border px-3 py-2 text-sm"
          />
          <input
            placeholder="Description"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            className="col-span-2 rounded border px-3 py-2 text-sm"
          />
          <button
            type="submit"
            className="col-span-2 rounded bg-blue-600 py-1.5 text-sm font-medium text-white hover:bg-blue-700"
          >
            Create (starts in INTAKE)
          </button>
        </form>
      )}

      <select
        value={statusFilter}
        onChange={(e) => setStatusFilter(e.target.value)}
        className="rounded border px-3 py-2 text-sm"
      >
        <option value="">All statuses</option>
        {STATUSES.map((s) => (
          <option key={s} value={s}>
            {s}
          </option>
        ))}
      </select>

      <div className="overflow-x-auto rounded-lg border bg-white">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-left text-gray-500">
            <tr>
              <th className="p-2">Model</th>
              <th className="p-2">Make</th>
              <th className="p-2">Status</th>
              <th className="p-2">Condition</th>
              <th className="p-2">Set status</th>
            </tr>
          </thead>
          <tbody>
            {data?.results.map((toy) => (
              <tr key={toy.id} className="border-t">
                <td className="p-2">{toy.model_name}</td>
                <td className="p-2">{toy.make}</td>
                <td className="p-2">{toy.status}</td>
                <td className="p-2">{toy.condition}</td>
                <td className="p-2">
                  <select
                    value=""
                    onChange={(e) => e.target.value && transition(toy.id, e.target.value)}
                    className="rounded border px-2 py-1 text-xs"
                  >
                    <option value="">Transition…</option>
                    {STATUSES.map((s) => (
                      <option key={s} value={s}>
                        {s}
                      </option>
                    ))}
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
