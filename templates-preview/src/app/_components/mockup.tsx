export function Mockup({
  label,
  ratio = "4 / 5",
  className = "",
}: {
  label: string;
  ratio?: string;
  className?: string;
}) {
  return (
    <div
      className={`flex items-center justify-center rounded-2xl border border-dashed border-black/20 bg-[repeating-linear-gradient(135deg,rgba(0,0,0,.05)_0px,rgba(0,0,0,.05)_10px,transparent_10px,transparent_20px)] text-center text-xs font-medium text-black/40 ${className}`}
      style={{ aspectRatio: ratio }}
    >
      <span className="px-3">{label}</span>
    </div>
  );
}
