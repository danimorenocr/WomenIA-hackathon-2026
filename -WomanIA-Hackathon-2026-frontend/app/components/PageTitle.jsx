export default function PageTitle({ title, subtitle }) {
  return (
    <div className="m-10 flex items-start gap-4">

  <span className="w-1 self-stretch bg-[#0D2340] rounded-full"></span>

  <div>
    <h1 className="text-3xl font-bold text-slate-900">
      {title}
    </h1>

    {subtitle && (
      <p className="text-slate-500 mt-1">
        {subtitle}
      </p>
    )}
  </div>

</div>
  )
}

