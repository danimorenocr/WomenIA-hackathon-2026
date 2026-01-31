export default function KPIBox({ title, value }) {
  return (
    <div className="bg-[#BCBEDA] rounded-2xl p-5 flex flex-col justify-center items-center">
        <h2 className="text-4xl font-bold">{value}</h2>
        <p className="text-sm text-slate-700">{title}</p>
      
    </div>
  );
}