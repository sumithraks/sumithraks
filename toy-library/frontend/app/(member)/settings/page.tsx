"use client";

import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { apiFetch, ApiError } from "@/lib/api-client";
import { subscribeToPush } from "@/lib/push";

type NotificationPreference = {
  email_enabled: boolean;
  push_enabled: boolean;
  due_date_reminders: boolean;
  waitlist_alerts: boolean;
  reservation_alerts: boolean;
  billing_alerts: boolean;
};

export default function SettingsPage() {
  const queryClient = useQueryClient();
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [enrollData, setEnrollData] = useState<{ otpauth_uri: string; qr_code_png_base64: string } | null>(
    null
  );
  const [confirmCode, setConfirmCode] = useState("");
  const [recoveryCodes, setRecoveryCodes] = useState<string[] | null>(null);

  const { data: preference } = useQuery({
    queryKey: ["notification-preference"],
    queryFn: () => apiFetch<NotificationPreference>("/notification-preferences/me/"),
  });

  const reset = () => {
    setError("");
    setMessage("");
  };

  const togglePreference = async (key: keyof NotificationPreference, value: boolean) => {
    reset();
    try {
      await apiFetch("/notification-preferences/me/", { method: "PATCH", body: { [key]: value } });
      queryClient.invalidateQueries({ queryKey: ["notification-preference"] });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not update preference");
    }
  };

  const enroll2fa = async () => {
    reset();
    try {
      const data = await apiFetch<{ otpauth_uri: string; qr_code_png_base64: string }>(
        "/auth/2fa/enroll/",
        { method: "POST" }
      );
      setEnrollData(data);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not start 2FA enrollment");
    }
  };

  const confirm2fa = async () => {
    reset();
    try {
      const data = await apiFetch<{ recovery_codes: string[] }>("/auth/2fa/confirm/", {
        method: "POST",
        body: { code: confirmCode },
      });
      setRecoveryCodes(data.recovery_codes);
      setEnrollData(null);
      setMessage("Two-factor authentication enabled.");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Invalid code");
    }
  };

  const disable2fa = async () => {
    reset();
    try {
      await apiFetch("/auth/2fa/disable/", { method: "POST" });
      setMessage("Two-factor authentication disabled.");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not disable 2FA");
    }
  };

  const enablePush = async () => {
    reset();
    try {
      await subscribeToPush();
      setMessage("Push notifications enabled on this device.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not enable push notifications");
    }
  };

  return (
    <div className="max-w-xl space-y-6">
      <h1 className="text-2xl font-semibold">Settings</h1>
      {message && <p className="rounded bg-green-50 p-2 text-sm text-green-700">{message}</p>}
      {error && <p className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</p>}

      <section className="rounded-lg border bg-white p-4">
        <h2 className="mb-2 font-medium text-gray-700">Two-factor authentication</h2>
        {!enrollData && !recoveryCodes && (
          <div className="flex gap-2">
            <button
              onClick={enroll2fa}
              className="rounded bg-blue-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-blue-700"
            >
              Enable 2FA
            </button>
            <button
              onClick={disable2fa}
              className="rounded border px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Disable 2FA
            </button>
          </div>
        )}
        {enrollData && (
          <div className="space-y-3">
            <p className="text-sm text-gray-600">Scan this QR code with your authenticator app:</p>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={`data:image/png;base64,${enrollData.qr_code_png_base64}`}
              alt="2FA QR code"
              className="h-40 w-40"
            />
            <input
              placeholder="Enter code from app"
              value={confirmCode}
              onChange={(e) => setConfirmCode(e.target.value)}
              className="w-full rounded border px-3 py-2 text-sm"
            />
            <button
              onClick={confirm2fa}
              className="rounded bg-blue-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-blue-700"
            >
              Confirm
            </button>
          </div>
        )}
        {recoveryCodes && (
          <div className="rounded bg-yellow-50 p-3 text-sm">
            <p className="mb-2 font-medium">Save these recovery codes somewhere safe:</p>
            <ul className="grid grid-cols-2 gap-1 font-mono text-xs">
              {recoveryCodes.map((code) => (
                <li key={code}>{code}</li>
              ))}
            </ul>
          </div>
        )}
      </section>

      <section className="rounded-lg border bg-white p-4">
        <h2 className="mb-2 font-medium text-gray-700">Push notifications</h2>
        <button
          onClick={enablePush}
          className="rounded bg-blue-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-blue-700"
        >
          Enable push on this device
        </button>
      </section>

      <section className="rounded-lg border bg-white p-4">
        <h2 className="mb-2 font-medium text-gray-700">Notification preferences</h2>
        {preference && (
          <div className="space-y-2 text-sm">
            {(
              [
                ["email_enabled", "Email notifications"],
                ["push_enabled", "Push notifications"],
                ["due_date_reminders", "Due date reminders"],
                ["waitlist_alerts", "Waitlist alerts"],
                ["reservation_alerts", "Reservation alerts"],
                ["billing_alerts", "Billing alerts"],
              ] as [keyof NotificationPreference, string][]
            ).map(([key, label]) => (
              <label key={key} className="flex items-center justify-between">
                <span>{label}</span>
                <input
                  type="checkbox"
                  checked={preference[key]}
                  onChange={(e) => togglePreference(key, e.target.checked)}
                />
              </label>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
