#!/usr/bin/env python
from ROOT import TCanvas, TFile, TLegend, gStyle


# superimposed reco and gen distributions per specie
def specie_distribution(had, var):
    fileo2 = TFile("../codeHF/AnalysisResults_O2.root")
    gStyle.SetOptStat(0)
    cpt = TCanvas("cpt", "pT distribution")
    cpt.SetCanvasSize(1500, 700)
    cpt.Divide(2, 1)
    hnum = fileo2.Get("qa-tracking-efficiency-%s/%s/num" % (had, var))
    hden = fileo2.Get("qa-tracking-efficiency-%s/%s/den" % (had, var))
    hden.Rebin(4)
    hnum.Rebin(4)
    hnum.SetLineColor(6)
    hden.GetYaxis().SetRangeUser(
        0.7 * hnum.GetBinContent(hden.GetMinimumBin()),
        1.3 * hden.GetBinContent(hden.GetMaximumBin()),
    )
    hden.Draw()
    hnum.Draw("same")
    hden.SetTitle("%s tracks %s distribution" % (had, var))
    leg = TLegend(0.7, 0.7, 0.9, 0.9, "")
    leg.SetFillColor(0)
    leg.AddEntry(hnum, "Rec. Level")
    leg.AddEntry(hden, "Gen. Level")
    leg.Draw()
    cpt.SaveAs("%sdistribution_hfcand%s.pdf" % (var, had))
    cpt.SaveAs("%sdustribution_hfcand%s.root" % (var, had))


def multiplicity():
    fileo2 = TFile("../codeHF/AnalysisResults_O2.root")
    cmult = TCanvas("cmult", "mult distribution")
    cmult.SetCanvasSize(1500, 700)
    cmult.SetLogy()
    cmult.Divide(2, 1)
    hmult = fileo2.Get("qa-global-observables/multiplicity/numberOfTracks")
    hmult.Rebin(4)
    hmult.Draw()
    hmult.SetTitle("Multiplicity Distribution")
    cmult.SaveAs("multiplicity.pdf")
    cmult.SaveAs("multiplicity.root")


def var_tracking(var):
    fileo2 = TFile("../codeHF/AnalysisResults_O2.root")
    cvar = TCanvas("cvar", "var distribution")
    cvar.SetCanvasSize(1500, 700)
    cvar.Divide(2, 1)
    hvar = fileo2.Get("qa-tracking-kine/tracking/%s" % var)
    hvar.Rebin(4)
    hvar.Draw()
    cvar.SaveAs("tracking_%s.pdf" % var)
    cvar.SaveAs("tracking_%s.root" % var)


def tracking_resolution(var1, mode, var2, var3):
    fileo2 = TFile("../codeHF/AnalysisResults_O2.root")
    cres = TCanvas("cres", "resolution distribution")
    cres.SetCanvasSize(1500, 700)
    if var1 == "eta":
        heta = fileo2.Get("qa-tracking-resolution/eta/etaDiffMCRecoVsEta%s" % mode)
        heta.Draw("coltz")
        heta.SetTitle("#eta resolution")
        cres.SaveAs("Resolution_%s_%s.pdf" % (var1, var2))
        cres.SaveAs("Resolution_%s_%s.root" % (var1, var2))
    if var1 == "impactParameter":
        himp_par = fileo2.Get(
            "qa-tracking-resolution/%s/%s%sVs%s" % (var1, var1, var2, var3)
        )
        himp_par.Draw("coltz")
        himp_par.SetTitle("Impact Parameter resolution: %s Vs %s" % (var2, var3))
        cres.SaveAs("impact_parameter_resolution%sVs%s.pdf" % (var2, var3))
    if var1 == "impactParameterError":
        himp_par_err = fileo2.Get(
            "qa-tracking-resolution/impactParameter/%s%sVs%s" % (var1, var2, var3)
        )
        himp_par_err.Draw("coltz")
        himp_par_err.SetTitle(
            "Impact Parameter Error resolution: %s Vs %s" % (var2, var3)
        )
        cres.SaveAs("impactParameterError_resolution%sVs%s.pdf" % (var2, var3))
    if var1 == "phi":
        hphi = fileo2.Get("qa-tracking-resolution/phi/phiDiffMCRec")
        hphi.Draw()
        hphi.SetTitle("#phi resolution")
        cres.SaveAs("phi_resolution.pdf")
        cres.SaveAs("phi_resolution.root")
    if var1 == "pt":
        h_pt = fileo2.Get("qa-tracking-resolution/pt/ptResolutionVs%s" % var2)
        h_pt.Draw("coltz")
        h_pt.SetTitle("p_{T} resolution")
        cres.SaveAs("ptResolutionVs%s.pdf" % var2)
        cres.SaveAs("ptResolutionVs%s.root" % var2)


def vertex_distributions(var):
    fileo2 = TFile("../codeHF/AnalysisResults_O2.root")
    cvertex = TCanvas("cvertex", "vertex ")
    cvertex.SetCanvasSize(1500, 700)
    cvertex.Divide(2, 1)
    hvertex = fileo2.Get("qa-global-observables/collision/%s" % var)
    cvertex.cd(1)
    hvertex.Draw()
    hvertex_res = fileo2.Get("qa-global-observables/collision/%svsNContrib" % var)
    cvertex.cd(2)
    hvertex_res.Draw("coltz")
    cvertex.SaveAs("vertex_%s.pdf" % var)
    cvertex.SaveAs("vertex_%s.root" % var)


multiplicity()
specie_distribution("pion", "pt")
specie_distribution("proton", "pt")
specie_distribution("electron", "pt")
specie_distribution("muon", "pt")
specie_distribution("kaon", "eta")
specie_distribution("pion", "eta")
specie_distribution("proton", "eta")
specie_distribution("electron", "eta")
specie_distribution("muon", "eta")
specie_distribution("kaon", "phi")
specie_distribution("pion", "phi")
specie_distribution("proton", "phi")
specie_distribution("electron", "phi")
specie_distribution("muon", "phi")
vertex_distributions("X")
vertex_distributions("Y")
vertex_distributions("Z")
var_tracking("eta")
tracking_resolution("eta", "MC", "", "")
tracking_resolution("impactParameter", "", "RPhi", "Pt")
tracking_resolution("impactParameter", "", "RPhi", "Phi")
tracking_resolution("impactParameter", "", "RPhi", "Eta")
tracking_resolution("impactParameter", "", "Z", "Pt")
tracking_resolution("impactParameter", "", "Z", "Phi")
tracking_resolution("impactParameter", "", "Z", "Eta")
tracking_resolution("impactParameterError", "", "RPhi", "Pt")
tracking_resolution("impactParameterError", "", "RPhi", "Phi")
tracking_resolution("impactParameterError", "", "RPhi", "Eta")
tracking_resolution("impactParameterError", "", "Z", "Pt")
tracking_resolution("impactParameterError", "", "Z", "Phi")
tracking_resolution("impactParameterError", "", "Z", "Eta")
tracking_resolution("pt", "", "Eta", "")
