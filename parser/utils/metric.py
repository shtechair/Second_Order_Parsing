# -*- coding: utf-8 -*-
import pdb

class Metric(object):

    def __init__(self, eps=1e-5):
        super(Metric, self).__init__()

        self.eps = eps
        self.total = 0.0
        self.correct_arcs = 0.0
        self.correct_rels = 0.0

        self.total_tree = 0.0
        self.correct_utree = 0.0
        self.correct_ltree = 0.0

    def __repr__(self):
        return f"UAS: {self.uas:6.2%} LAS: {self.las:6.2%} UEM: {self.uem:6.2%} LEM: {self.lem:6.2%}"

    def __call__(self, arc_preds, rel_preds, arc_golds, rel_golds, mask):
        arc_mask = arc_preds.eq(arc_golds)[mask]
        rel_mask = rel_preds.eq(rel_golds)[mask] & arc_mask

        self.total += len(arc_mask)
        self.correct_arcs += arc_mask.sum().item()
        self.correct_rels += rel_mask.sum().item()
        self.total_tree += len(arc_preds)
        arc_mask = arc_preds.eq(arc_golds)*mask
        rel_mask = rel_preds.eq(rel_golds)*mask & arc_mask
        gold_num = mask.sum(-1)
        arc_res = arc_mask.sum(-1)
        rel_res = rel_mask.sum(-1)
        self.correct_utree += arc_res.eq(gold_num).sum().item()
        self.correct_ltree += rel_res.eq(gold_num).sum().item()

    def __lt__(self, other):
        return self.score < other

    def __le__(self, other):
        return self.score <= other

    def __ge__(self, other):
        return self.score >= other

    def __gt__(self, other):
        return self.score > other

    @property
    def score(self):
        return self.las

    @property
    def uas(self):
        return self.correct_arcs / (self.total + self.eps)

    @property
    def las(self):
        return self.correct_rels / (self.total + self.eps)

    @property
    def uem(self):
        return self.correct_utree / (self.total_tree + self.eps)

    @property
    def lem(self):
        return self.correct_ltree / (self.total_tree + self.eps)

